from cement.core import backend
from skyler import Skyler

defaults = backend.defaults('base', 'keystone')
defaults['base']['rabbitmq_host'] = 'localhost'
defaults['base']['rabbitmq_user'] = 'guest'
defaults['base']['rabbitmq_password'] = 'pass'

defaults['base']['heat_endpoint'] = 'http://localhost:8004/'
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
