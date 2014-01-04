#!/usr/bin/env bash
set -x

yum install -y python-setuptools
easy_install pip
pip install virtualenv --no-use-wheel -v
