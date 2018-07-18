#!/bin/bash
python3 -m pip install --user --upgrade setuptools wheel
cd ./gocryptsyncthing/
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
cd ..
python3 -m pip install --index-url https://test.pypi.org/simple/ example_pkg
