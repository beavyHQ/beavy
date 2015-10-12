#!/bin/bash
set -e

for path in tests/apps/*; do
    app=$(basename "$path")
    echo "Building $app"
    psql -c "drop database if exists test_$app;" -U postgres
    psql -c "create database test_$app;" -U postgres
    cp -f "$path/config.yml" config.yml
    python manager.py db upgrade heads
    npm run build
    mv build/public "build/$app"
done