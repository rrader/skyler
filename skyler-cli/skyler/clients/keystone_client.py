import keystoneclient.v2_0.client as ksclient

from skyler.conf import CONFIG
from skyler.utils import classproperty


class Keystone(object):
    _client = None

    @classproperty
    def client(cls):
        if not Keystone._client:
            Keystone.connect()
        return Keystone._client

    @staticmethod
    def connect():
        Keystone._client = ksclient.Client(auth_url=CONFIG.get('keystone', 'auth_url'),
                                           username=CONFIG.get('keystone', 'username'),
                                           password=CONFIG.get('keystone', 'password'),
                                           tenant_name=CONFIG.get('keystone', 'tenant'))
