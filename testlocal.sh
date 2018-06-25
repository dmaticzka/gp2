#!/usr/bin/env bash

DIRS="gp2 test"

echo "### flake8 ####################################################"
flake8 $DIRS --ignore=E501

#echo
#echo "### pylint ####################################################"
#pylint --py3k eden test

echo
echo "### pytest ####################################################"
PYTHONHASHSEED=0 pytest $DIRS --cov gp2 --doctest-modules
