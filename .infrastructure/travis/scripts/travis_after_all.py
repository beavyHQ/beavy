from functools import reduce
import urllib.request as urllib2

import json
import time
import os


travis_entry = 'https://api.travis-ci.org'
build_id = os.getenv("TRAVIS_BUILD_ID")
polling_interval = int(os.getenv("POLLING_INTERVAL", '5'))
gh_token = os.getenv("GITHUB_TOKEN")
job_number = os.getenv("TRAVIS_JOB_NUMBER")

is_leader = lambda job: job.endswith('.1')

if not job_number:
    # seems even for builds with only one job, this won't get here
    print("Don't use defining leader for build without matrix")
    exit(1)
elif not is_leader(job_number):
    print("not the leader")
    exit(1)


class MatrixElement(object):
    def __init__(self, json_raw):
        self.is_finished = json_raw['finished_at'] is not None
        self.is_succeeded = json_raw['result'] == 0
        self.number = json_raw['number']
        self.is_leader = is_leader(self.number)


def matrix_snapshot(travis_token):
    """
    :return: Matrix List
    """
    headers = {'content-type': 'application/json', 'Authorization': 'token {}'.format(travis_token)}
    req = urllib2.Request("{0}/builds/{1}".format(travis_entry, build_id), headers=headers)
    response = urllib2.urlopen(req).read().decode("utf-8")
    raw_json = json.loads(response)
    matrix_without_leader = [MatrixElement(job) for job in raw_json["matrix"] if not is_leader(job['number'])]
    return matrix_without_leader


def wait_others_to_finish(travis_token):
    def others_finished():
        """
        Dumps others to finish
        Leader cannot finish, it is working now
        :return: tuple(True or False, List of not finished jobs)
        """
        snapshot = matrix_snapshot(travis_token)
        finished = [job.is_finished for job in snapshot if not job.is_leader]
        return reduce(lambda a, b: a and b, finished), [job.number for job in snapshot if
                                                        not job.is_leader and not job.is_finished]

    while True:
        finished, waiting_list = others_finished()
        if finished:
            break
        print("Leader waits for minions {0}...".format(waiting_list))  # just in case do not get "silence timeout"
        time.sleep(polling_interval)


def get_token():
    assert gh_token, 'GITHUB_TOKEN is not set'
    data = {"github_token": gh_token}
    headers = {'content-type': 'application/json'}

    req = urllib2.Request("{0}/auth/github".format(travis_entry), json.dumps(data).encode("utf-8"), headers)
    response = urllib2.urlopen(req).read().decode("utf-8")
    travis_token = json.loads(response).get('access_token')

    return travis_token


token = get_token()
wait_others_to_finish(token)

final_snapshot = matrix_snapshot(token)
print("Final Results: {0}".format([(e.number, e.is_succeeded) for e in final_snapshot]))

others_snapshot = [el for el in final_snapshot if not el.is_leader]
if reduce(lambda a, b: a and b, [e.is_succeeded for e in others_snapshot]):
    print("Succeeded – continue.")
    exit(0)
