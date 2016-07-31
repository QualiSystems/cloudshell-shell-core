#!/usr/bin/env bash
echo Installing depdendencies

if [ "${TRAVIS_BRANCH}" = "master" ]
then
    pip install -r requirements.txt
    pip install cloudshell-automation-api>=7.0.0.0,<7.1.0.0
    echo Installing depdendencies2
else
    pip install -r requirements.txt --extra-index-url https://testpypi.python.org/simple
    pip install cloudshell-automation-api>=7.0.0.0,<7.1.0.0 --extra-index-url https://testpypi.python.org/simple
    echo Installing depdendencies3
fi

pip install -r test_requirements.txt
pip install coveralls
echo Installing depdendencies4

