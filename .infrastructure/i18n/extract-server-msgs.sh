#!/bin/bash

# This needs to be run from beavy root like so:
#     `./.infrastructure/i18n/extract-server-messages.sh`
# Otherwise the working directory will be wrong.

# Extraction
pybabel extract -F babel.cfg -k format -k format_time -k format_date -k format_datetime -k format_number -k format_currency -k format_decimal -k format_percent -o messages.pot .
pybabel init -i messages.pot -d . -o './beavy-server.po' -l en
mkdir var/server-messages
./node_modules/.bin/po2json beavy-server.po var/server-messages/beavy-server.json -F -f mf --fallback-to-msgid

# Clean up
rm messages.pot
rm beavy-server.po
