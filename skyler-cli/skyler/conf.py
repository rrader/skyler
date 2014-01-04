from cement.core import backend
from skyler import Skyler

defaults = backend.defaults('base', 'keystone')
defaults['base']['rabbitmq_host'] = 'localhost'
defaults['base']['rabbitmq_user'] = 'guest'
defaults['base']['rabbitmq_password'] = 'pass'

defaults['base']['heat_endpoint'] = 'http://10.0.2.15:8004/v1'
defaults['base']['templates'] = '/vagrant/skyler-cli/skyler/templates'
defaults['base']['docker-registry'] = 'localhost:5042'

defaults['base']['neutron_endpoint'] = 'http://localhost:9696/'
# defaults['base']['network'] = 'sky-net'
defaults['base']['subnet'] = 'private-subnet'
defaults['base']['network'] = 'private'
# defaults['base']['cidr_start'] = '10.0.1.0/28'
# defaults['base']['gateway'] = '10.0.1.1'

# TODO: remove this from conf, read from env vars
defaults['keystone']['auth_url'] = 'http://localhost:35357/v2.0'
defaults['keystone']['username'] = 'admin'
defaults['keystone']['password'] = 'pass'
defaults['keystone']['tenant'] = 'demo'

app = Skyler('skyler', config_defaults=defaults)
app.setup()
CONFIG = app.config
app.close()
