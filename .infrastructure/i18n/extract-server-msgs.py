import os

# Keys indicating the fn symbols that pybabel should search for
# when finding translations.
keys = '-k format -k format_time -k format_date -k format_datetime'

# Extraction
os.system("pybabel extract -F babel.cfg {} -o messages.pot .".format(keys))
os.system("pybabel init -i messages.pot -d . -o './beavy-server.po' -l en")
os.system("./node_modules/.bin/po2json beavy-server.po var/server-messages/beavy-server.json -F -f mf --fallback-to-msgid")

# Clean up
os.system("rm messages.pot")
os.system("rm beavy-server.po")
