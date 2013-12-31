import keystoneclient.v2_0.client as ksclient

from heatclient.client import Client
from conf import CONFIG


class Heat(object):
    _client = None
    _keystone = None

    @property
    def client(self):
        if not Heat._client:
            self.connect()
        return self._client

    def connect(self):
        self._keystone = ksclient.Client(auth_url=CONFIG.get('keystone', 'auth_url'),
                                         username=CONFIG.get('keystone', 'username'),
                                         password=CONFIG.get('keystone', 'password'),
                                         tenant_name=CONFIG.get('keystone', 'tenant'))

        self._client = Client('1', endpoint="{}/{}".format(CONFIG.get('base', 'heat_endpoint'),
                                                              self._keystone.tenant_id),
                              token=self._keystone.auth_token)
