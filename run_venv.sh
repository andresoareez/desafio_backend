#!/bin/bash

python3 -m venv api-env
source api-env/bin/activate
pip install dnspython
pip install -r requirements.txt
