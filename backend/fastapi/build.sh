#!/usr/bin/env sh
set -x
here=$(dirname "$(realpath "$0")")
cd "${here}" || exit
rm -rf local/build local/dist
mkdir -p local/build local/dist
cp ./*.py local/build
cp -r ./api local/build
rm -rf local/build/server.py
find local/build -type d -name '__pycache__' -exec rm -rf {} \;
find local/build -type f -name 'test_*.py' -exec rm -rf {} \;
cd local/build && zip -r9 ../dist/package.zip ./*
cd "${here}" || exit
rm -rf local/build
