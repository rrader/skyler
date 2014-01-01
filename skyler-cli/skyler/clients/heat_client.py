from skyler.clients.keystone_client import Keystone

from heatclient.client import Client

from skyler.conf import CONFIG
from skyler.utils import classproperty


class Heat(object):
    _client = None

    @classproperty
    def client(cls):
        if not Heat._client:
            Heat.connect()
        return Heat._client

    @staticmethod
    def connect():
        keystone = Keystone.client

        Heat._client = Client('1', endpoint="{}/{}".format(CONFIG.get('base', 'heat_endpoint'),
                                                           keystone.tenant_id),
                              token=keystone.auth_token)
