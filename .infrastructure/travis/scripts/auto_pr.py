import os
import sys
import json
import time
import logging

import urllib.request as urllib2
from urllib.error import HTTPError

REPO = "beavyHQ/beavy"
BRANCHES = ("master", )

log = logging.getLogger("travis.leader")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

if os.getenv("TRAVIS_PULL_REQUEST") != 'false':
    print("We are building a PR – Skipping")
    sys.exit(0)

branch = os.getenv('TRAVIS_BRANCH')
repo = os.getenv('TRAVIS_REPO_SLUG')
gh_token = os.getenv('GITHUB_TOKEN', None)

if repo != REPO or branch not in BRANCHES:
    print("We only autodeploy from travis when building {} of {}".format(",".join(BRANCHES), REPO))
    sys.exit(0)
elif not gh_token:
    print("{} not found. exiting.".format(GITHUB_TOKEN))
    sys.exit(0)

user = repo.split('/')[0]

BASE_HEADERS ={
        'Authorization': 'token {}'.format(gh_token),
        'content-type': 'application/json'
    }


def query_github(query, payload={}, **headers):
    headers.update(BASE_HEADERS)
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib2.Request("https://api.github.com{0}".format(query),
                          data, headers)
    resp = json.loads(urllib2.urlopen(req).read().decode("utf-8"))
    return resp

print(" – Fetching forks")

for fork in query_github("/repos/{0}/forks".format(repo)):
    full_name = fork["full_name"]
    default_branch = fork["default_branch"]

    if default_branch == 'master':
        print("Skipping {} – it's set to master.".format(full_name))
        continue

    pulls = query_github("/repos/{0}/pulls?open=true&head={1}:{2}".format(
                         full_name, repo, branch))

    if pulls:
        print("Skipping {} – it still has a PR pending (which should update automagically)".format(full_name))
        continue

    try:
        pr = query_github("/repos/{0}/pulls".format(full_name), {
            "title": "✨ Merge new upstream updates ✨",
            "head": "{}:{}".format(user, branch),
            "base": default_branch,
# FIXME: make this more specific to the PR itself
# FIXME: switch this to an automatic bot
# FIXME: add link to docs about this, and allow ppl to turn this off
        "body": """Hello,

We've made a lot of improvements on the upstream version of the beavy project.
You might want to consider merging them in. This PR contains the latest state
we have upstream.

If something breaks, we'd appreciate if you could let us know about it.

Thanks!
Beavy

-----
This is an automatic service provided to you as you forked the repo and
switched the default branch – thus making us believe you are building
your own version on top of beavy.
"""

        })
    except HTTPError as exc:
        print("Error {0} – sending PR failed: {1}".format(full_name, exc))
    else:
        print("Success {0} – PR send for {1} {2} ".format(full_name, default_branch, pr["url"]))
