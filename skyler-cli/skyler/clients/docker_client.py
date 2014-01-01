import docker
from skyler.utils import classproperty


class Docker(object):
    _client = None

    @classproperty
    def client(cls):
        if not Docker._client:
            Docker.connect()
        return Docker._client

    @staticmethod
    def connect():
        Docker._client = docker.Client(base_url='unix://var/run/docker.sock',
                                       version='1.6',
                                       timeout=None)
