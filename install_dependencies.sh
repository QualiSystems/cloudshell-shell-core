#!/usr/bin/env bash
if [ "${TRAVIS_BRANCH}" = "master" ]; then
    pip install -r requirements.txt
    pip install cloudshell-automation-api>=7.0.0.0,<7.1.0.0
else
    pip install -r requirements.txt --index-url https://testpypi.python.org/simple
    pip install cloudshell-automation-api>=7.0.0.0,<7.1.0.0 --index-url https://testpypi.python.org/simple
fi

pip install -r test_requirements.txt
pip install coveralls
