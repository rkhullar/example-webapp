#!/usr/bin/env sh

set -x
here=$(dirname "$(realpath "$0")")

backend_path="${here}/backend/fastapi"
cd "${backend_path}" || exit
rm -rf venv
python -m venv venv
. venv/bin/activate
pip install -U pip setuptools
pip install pipenv
pipenv install --dev
