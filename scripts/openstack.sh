#!/usr/bin/env bash

set -x

if [[ -f /opt/openstack-installed ]]; then
    su - stack -c"bash /opt/devstack/rejoin-stack.sh"
else
    apt-get update
    apt-get -y install curl git wget socat


    # # kill me. don't ask me how I've googled it
    # # https://www.mail-archive.com/openstack@lists.launchpad.net/msg21895.html
    # modprobe -r bridge || true
    # apt-get -y install openvswitch-switch openvswitch-controller openvswitch-brcompat
    # echo "blacklist bridge" > /etc/modprobe.d/bridge.conf
    # echo "BRCOMPAT=yes" >> /etc/default/openvswitch-switch

    # # http://www.brucemartins.com/2013_10_01_archive.html
    # apt-get install -y openvswitch-datapath-source
    # module-assistant auto-install openvswitch-datapath --non-inter --quiet  # FIXME: no tty
    # modprobe -r bridge || true
    # service openvswitch-switch restart



    cd /opt;
    git clone https://github.com/antigluk/devstack.git; cd devstack
    git checkout docker-downgrade
    source lib/nova_plugins/hypervisor-docker
    if [[ ! -r /vagrant/.cache/docker-registry.tar.gz ]]; then
        wget -O /vagrant/.cache/docker-registry.tar.gz ${DOCKER_REGISTRY_IMAGE};
    fi
    cp /vagrant/.cache/docker-registry.tar.gz files/
    ./tools/docker/install_docker.sh
    ./tools/create-stack-user.sh
    usermod -a -G docker stack
    mkdir /var/log/openstack && chown stack:stack /var/log/openstack;
    cp /vagrant/scripts/localrc /opt/devstack/localrc
    chown stack:stack -R /opt/devstack
    su - stack -c"export PIP_DOWNLOAD_CACHE=/vagrant/.cache && bash /opt/devstack/stack.sh"
    echo "export OS_USERNAME=admin" >> openrc
    echo "export OS_TENANT_NAME=admin" >> openrc
    echo "export OS_PASSWORD=pass" >> openrc
    echo "export OS_AUTH_URL=http://127.0.0.1:5000/v2.0/" >> openrc
    echo "export PS1='[\u@\h \W(keystone_admin)]\$ '" >> openrc

    #Docker plugin for Heat
    # TODO: remove this plugin (it works without Nova that is not appropriate)
    mkdir /usr/lib/heat
    chown stack:stack -R /usr/lib/heat
    su - stack -c"mkdir -p /opt/stack/heat"
    cd /opt/stack
    su - stack -c"git clone https://github.com/dotcloud/openstack-heat-docker.git"
    su - stack -c"ln -sf $(cd openstack-heat-docker/plugin; pwd) /usr/lib/heat/docker"

    su - stack -c"cd /opt/devstack && source openrc && nova keypair-add default > default.pem && chmod 600 default.pem"

    source /opt/devstack/openrc
    SUBNET=$(neutron subnet-list | grep private-subnet | awk '{ print $2 }')
    

    # create neutron network
    # FIXME: for now disabled
    # neutron net-create sky-net

    # install skyler
    mkdir /var/lib/skyler
    chown stack:stack -R /var/lib/skyler

    mkdir -p /opt/stack/skyler
    virtualenv /opt/stack/skyler/venv
    chown stack:stack -R /opt/stack/skyler
    source /opt/stack/skyler/venv/bin/activate
    pip install git+git://github.com/dotcloud/docker-py.git#egg=docker-py
    pip install six>=1.4.1
    cd /vagrant/skyler-cli/
    pip install -e .
    skyler init
    skyler create-app example /vagrant/examples/flaskexample

    touch /opt/openstack-installed
fi
