FROM ubuntu:12.04

# SSH
EXPOSE 22
RUN apt-get update
RUN apt-get -y install openssh-server sudo wget
RUN mkdir -p /var/run/sshd
RUN sed 's/UsePAM yes/UsePAM no/' -i /etc/ssh/sshd_config
RUN sed 's/#PermitRootLogin yes/PermitRootLogin yes/' -i /etc/ssh/sshd_config
RUN sed 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' -i /etc/ssh/sshd_config
RUN /usr/sbin/sshd


RUN apt-get -y install haproxy


ADD haproxy.cfg /haproxy/haproxy.cfg
ADD start /haproxy/start
RUN chmod 700 /haproxy/start


RUN useradd -m -d /home/haproxy haproxy
RUN echo 'root:1111' | chpasswd
RUN echo 'haproxy:1111' | chpasswd
RUN su - haproxy -c "mkdir -p /home/haproxy/.ssh"
ADD start.sh /home/haproxy/
RUN chmod +x /home/haproxy/start.sh
ADD id_rsa /home/haproxy/.ssh/
ADD id_rsa.pub /home/haproxy/.ssh/
# ADD known_hosts /home/haproxy/.ssh/
# ADD authorized_keys /home/haproxy/.ssh/
RUN chown haproxy:haproxy -R /home/haproxy/.ssh
RUN chmod 0700 /home/haproxy/.ssh && chmod 0600 /home/haproxy/.ssh/*


RUN sed 's/Defaults *requiretty/#Defaults    requiretty/' -i /etc/sudoers
RUN echo "haproxy ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN apt-get -y install git

ENTRYPOINT ["/home/haproxy/start.sh"]
