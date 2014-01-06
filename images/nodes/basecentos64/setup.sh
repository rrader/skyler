#!/usr/bin/env bash

yum clean all
yum -y install rsyslog openssh-server screen passwd sudo wget tar ntp bind-utils
sed 's/UsePAM yes/UsePAM no/' -i /etc/ssh/sshd_config
sed 's/#PermitRootLogin yes/PermitRootLogin yes/' -i /etc/ssh/sshd_config
/etc/init.d/sshd restart

adduser -d /var/lib/skyler skyler
echo 'root:1111' | chpasswd
echo 'skyler:1111' | chpasswd
su - skyler -c "mkdir /var/lib/skyler/.ssh"

cp /tmp/authorized_keys /var/lib/skyler/.ssh/
chown skyler:skyler -R /var/lib/skyler/.ssh
chmod 0700 /var/lib/skyler/.ssh && chmod 0600 /var/lib/skyler/.ssh/*

sed 's/Defaults *requiretty/#Defaults    requiretty/' -i /etc/sudoers
echo "skyler ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Fix /dev/fd
ln -s /proc/self/fd /dev/fd

su - skyler -c "mkdir /var/lib/skyler/app"
su - skyler -c "mkdir /var/lib/skyler/init.d"

rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
yum install -y cloud-init
sed "s/ec2-user/skyler/" -i /etc/cloud/cloud.cfg
sed "s/disable_root: 1/disable_root: 0/" -i /etc/cloud/cloud.cfg
sed "/\s-\sset_hostname/d" -i /etc/cloud/cloud.cfg

# Turn off iptables
/etc/init.d/iptables save
/etc/init.d/iptables stop
chkconfig iptables off

