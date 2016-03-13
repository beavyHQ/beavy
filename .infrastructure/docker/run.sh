#!/bin/bash
set -e
echo "starting $1"
# we do the weirdest hack of them all. if the "PORT" variable is exposed
# we _are_ the web process. so start web and otherwise, start the worker.
# see  https://github.com/dokku/dokku/blob/v0.4.14/dokku#L143-L159
cd /app
if [[ -n "$PORT" ]]; then
  echo "Running migrations"
  python manager.py db upgrade heads
  echo "Starting Web Service"
  start web
else
  echo "Starting Worker Service"
  start worker
fi
