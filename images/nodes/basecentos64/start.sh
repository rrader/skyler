#!/usr/bin/env bash
set -x

#
# Openstack docker hypervisor doesn't allow to define environment variables. For that reason we make use of the 
# provided metadata service.
#
# The metadata service is always available under the magic IP 169.254.169.254. It delivers a data blob.
# Our container assumes that the user data is a rc file which can be sourced by the main process. 

echo "== Openstack network configuration. Note: Containers expect to be in a 10.0.1.0/24 nova network. =="

# Hack: In order to receive data from the metadata service we must make sure we resolve the data via our nova network.
#
# A docker container in openstack has two NICs. 
# - eth0 has a IP address on the docker0 bridge which is usually an 172.0.0.0 IP address.
# - pvnetXXXX is a IP address assigned by nova.
#
# Extract the NIC name of the nova network.
#
NOVA_NIC=$(ip a | grep pvnet | head -n 1 | cut -d: -f2)

while [ "$NOVA_NIC" == "" ] ; do
   echo "Find nova NIC..."
   sleep 1
   NOVA_NIC=$(ip a | grep pvnet | head -n 1 | cut -d: -f2)
done

echo "Device $NOVA_NIC found. Wait until ready."
sleep 3

# Setup a network route to insure we use the nova network.
echo "[INFO] Create default route for $NOVA_NIC. Gateway 10.0.1.1"
ip r r default via 10.0.1.1 dev $NOVA_NIC
ip l set down dev eth0

echo "[INFO] Start Cloud init"
/usr/bin/cloud-init start

tail -50 /var/log/cloud-init.log;

echo "[INFO] Configuring and starting ssh"
SSH_L=`ifconfig $NOVA_NIC | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
echo "ListenAddress $SSH_L" >> /etc/ssh/sshd_config

# run other scripts
su - skyler -c "run-parts /var/lib/skyler/init.d"

/usr/sbin/sshd -D
