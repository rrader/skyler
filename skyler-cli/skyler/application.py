import datetime
from clients.keystone_client import Keystone
from clients.neutron_client import Neutron
from netaddr import IPNetwork
import os
from cement.core import controller
from texttable import Texttable
from utils import SkylerException
from db import Application, Session, Deployment, DEPLOYMENT_STATE_READABLE, DEPLOYMENT_STATE_BUILT_OK, DEPLOYMENT_STATE_SUCCESSFUL


class ApplicationListController(controller.CementBaseController):
    class Meta:
        label = 'app_list'
        description = 'application list'
        config_defaults = dict()
        arguments = []

    @controller.expose(hide=True, aliases=['list'])
    def default(self):
        self.log.info('List applications')
        table = Texttable()
        session = Session()
        table.add_row(('id', 'name', 'source', 'network-id'))
        for app in session.query(Application).all():
            table.add_row((app.id, app.name, app.source, app.network_id))
        print table.draw()


class ApplicationHistoryController(controller.CementBaseController):
    class Meta:
        label = 'history'
        description = 'deployment history'
        config_defaults = dict()
        arguments = [
            (['name'], dict(action='store', help='Application name')),
        ]

    @controller.expose(hide=True, aliases=['list'])
    def default(self):
        self.log.info('List deployments')
        table = Texttable()
        session = Session()
        table.add_row(('deployment', 'app', 'image', 'created', 'state'))
        for d in session.query(Deployment). \
            join(Application).filter(Application.name == self.pargs.name).all():
            table.add_row((d.id, d.application.name, d.image, d.created,
                           DEPLOYMENT_STATE_READABLE[d.state]))
        print table.draw()


class ApplicationCreationController(controller.CementBaseController):
    class Meta:
        label = 'create_app'
        description = 'application creation'

        config_defaults = dict()

        arguments = [
            (['name'], dict(action='store', help='Application name')),
            (['source'], dict(action='store', help='Source directory')), # TODO: change to git repo
        ]

    @controller.expose(help='Create new Skyler app')
    def default(self):
        self.log.info('Creating application')
        session = Session()
        app = Application(name=self.pargs.name, source=self.pargs.source)
        session.add(app)
        session.commit()


class ApplicationBuildController(controller.CementBaseController):
    class Meta:
        label = 'build'
        description = 'build machines'

        config_defaults = dict()

        arguments = [
            (['name'], dict(action='store', help='Application name')),
        ]

    @controller.expose(help='Build your Skyler app')
    def default(self):
        self.log.info('Building stack')
        session = Session()
        app = session.query(Application).filter(Application.name == self.pargs.name).first()
        if not app:
            self.log.error('No application found')
            raise SkylerException("No application found")
        runtime_name = file(os.path.join(app.source, 'runtime.txt')).read().strip()
        rt = getattr(__import__('skyler.runtime', fromlist=[runtime_name]), runtime_name)
        runtime = rt.Runtime(app.name)
        runtime.start_deploy()


class ApplicationSpinUpController(controller.CementBaseController):
    class Meta:
        label = 'spin_up'
        description = 'spin up your stack!'

        config_defaults = dict()

        arguments = [
            (['name'], dict(action='store', help='Application name')),
        ]

    def spin_up(self):
        session, target = self.get_deployment()
        heat = Heat.client
        heatfile = os.path.join(CONFIG.get('base', 'templates'), 'heat_template.txt')

        neutron = Neutron.client
        network = filter(lambda x: x['name'] == CONFIG.get('base', 'network'),
                         neutron.list_networks()['networks'])[0]

        params = {'date': datetime.datetime.now(),
                  'image_name': target.image,
                  'name': target.application.name,
                  'deployment_id': target.id,
                  'subnet': target.application.network_id,
                  'network': network['id']
        }
        heat_template = file(heatfile).read()
        heat_content = heat_template.format(**params)
        stack_name = '{}_d{}'.format(target.application.name, target.id)
        target.stack_name = stack_name
        #target.state = DEPLOYMENT_STATE_SUCCESSFUL
        session.add(target)
        self.log.info('Spinning up {}...'.format(stack_name))
        heat.stacks.create(stack_name=stack_name,
                           template=heat_content,
                           timeout_mins=60)
        session.commit()

    def get_deployment(self):
        session = Session()
        d = session.query(Deployment).join(Application).filter(Application.name == self.pargs.name)
        d = d.filter(Deployment.state == DEPLOYMENT_STATE_BUILT_OK)
        d = d.order_by(Deployment.id.desc())
        target = d.first()
        return session, target

    @controller.expose(help='Spin up your app!')
    def default(self):
        session, target = self.get_deployment()

        if not target:
            self.log.error('No successful builds found')
            raise SkylerException("No successful builds found")
        self.log.info('Last successful build #{}'.format(target.id))

        if not target.application.network_id:
            next_id = Neutron.find_new_id()
            neutron = Neutron.client
            net = IPNetwork(CONFIG.get('base', 'cidr_start')).next(next_id)

            network = filter(lambda x: x['name'] == CONFIG.get('base', 'network'),
                             neutron.list_networks()['networks'])[0]
            subnet_name = 'sky-{}'.format(target.application.name)
            self.log.info('Creating subnet {}'.format(subnet_name))
            ret = neutron.create_subnet(body=dict(subnet=dict(name=subnet_name,
                                                              network_id=network['id'],
                                                              ip_version='4',
                                                              cidr=str(net),
                                                              tenant_id=network['tenant_id'])))
            session = Session()
            app = session.query(Application).filter(Application.id == target.id).first()
            app.network_id = ret['subnet']['id']
            session.add(app)
            self.log.info('Subnet {} created'.format(app.network_id))
            session.commit()

        self.spin_up()
        self.log.info('Done')


from clients.heat_client import Heat
from conf import CONFIG
