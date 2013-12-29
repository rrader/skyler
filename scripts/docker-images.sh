#!/bin/bash

# generate keys
ssh-keygen -b 1024 -N '' -f /vagrant/dynokeys -t rsa -q
