#!/usr/bin/sh

echo "Installing virtual environment onto '.venv'"

virtualenv -p python3 .venv

echo "Entering virtual environment"

source .venv/bin/activate

echo "Installing pip requirements"

pip install -r requirements.txt

echo "Installing current package"

pip install .

echo "Running benchmark"

python3 merida/main.py
