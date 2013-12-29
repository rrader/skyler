#!/bin/bash

set -x

if [[ -f /opt/docker-images-built ]]; then
    echo "Docker images already built"
else

    DYNOKEYS=/vagrant/dynokeys

    # generate keys
    [ -f $DYNOKEYS ] || ssh-keygen -b 1024 -N '' -f $DYNOKEYS -t rsa -q

    #build base machine
    cp ${DYNOKEYS}.pub /vagrant/images/nodes/basecentos64/authorized_keys
    docker build -t skyler-basecentos64 /vagrant/images/nodes/basecentos64

    #build python 2.6 machine
    docker build -t skyler-python26 /vagrant/images/nodes/python2.6
    docker tag skyler-python26 localhost:5042/skyler-python26
    docker push localhost:5042/skyler-python26

    #TODO: build balancer

    touch /opt/docker-images-built
fi