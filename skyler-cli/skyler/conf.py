from cement.core import backend
from skyler import Skyler

defaults = backend.defaults('base', 'keystone')
defaults['base']['rabbitmq_host'] = 'localhost'
defaults['base']['rabbitmq_user'] = 'guest'
defaults['base']['rabbitmq_password'] = 'pass'

defaults['base']['heat_endpoint'] = 'http://10.0.2.15:8004/v1'
defaults['base']['templates'] = '/vagrant/skyler-cli/skyler/templates'
defaults['base']['docker-registry'] = 'localhost:5042'

defaults['keystone']['auth_url'] = 'http://localhost:35357/v2.0'
defaults['keystone']['username'] = 'admin'
defaults['keystone']['password'] = 'pass'
defaults['keystone']['tenant'] = 'demo'

app = Skyler('skyler', config_defaults=defaults)
app.setup()
CONFIG = app.config
app.close()
