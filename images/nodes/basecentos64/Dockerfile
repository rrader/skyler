FROM    centos:6.4

ADD setup.sh /tmp/setup.sh
ADD authorized_keys /tmp/

ADD setup.sh /tmp/
RUN /bin/bash /tmp/setup.sh

ADD start.sh /var/lib/skyler/

EXPOSE 22 80

CMD ["/bin/bash", "/var/lib/skyler/start.sh"]
