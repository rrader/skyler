import docker


class Docker(object):
    _client = None

    @property
    def client(self):
        if not Docker._client:
            self.connect()
        return self._client

    def connect(self):
        self._client = docker.Client(base_url='unix://var/run/docker.sock',
                                     version='1.6',
                                     timeout=None)
