from skyler.clients.keystone_client import Keystone

from neutronclient.neutron import client

from skyler.conf import CONFIG
from skyler.utils import classproperty


class Neutron(object):
    _client = None

    @classproperty
    def client(cls):
        if not Neutron._client:
            Neutron.connect()
        return Neutron._client

    @staticmethod
    def connect():
        keystone = Keystone.client
        Neutron._client = client.Client('2.0', endpoint_url=CONFIG.get('base', 'neutron_endpoint'),
                                        token=keystone.auth_token)

    @classmethod
    def find_new_id(cls):
        #FIXME
        return 0
