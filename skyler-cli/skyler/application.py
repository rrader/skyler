import os
from cement.core import controller
from db import Application, Session, Deployment
from texttable import Texttable
from utils import SkylerException


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
        table.add_row(('id', 'name', 'source'))
        for app in session.query(Application).all():
            table.add_row((app.id, app.name, app.source))
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
        table.add_row(('deployment', 'app', 'image', 'created'))
        for depl in session.query(Deployment).\
            join(Application).filter(Application.name == self.pargs.name).all():

            table.add_row((depl.id, depl.application.name, depl.image, depl.created))
        print table.draw()


class ApplicationCreationController(controller.CementBaseController):
    class Meta:
        label = 'create_app'
        description = 'application creation'

        config_defaults = dict()

        arguments = [
            (['name'], dict(action='store', help='Application name')),
            (['source'], dict(action='store', help='Source directory')),  # TODO: change to git repo
        ]

    @controller.expose(help='Create new Skyler app')
    def default(self):
        self.log.info('Creating application')
        session = Session()
        app = Application(name=self.pargs.name, source=self.pargs.source)
        session.add(app)
        session.commit()


class ApplicationSpinUpController(controller.CementBaseController):
    class Meta:
        label = 'spin_up'
        description = 'spin up your stack!'

        config_defaults = dict()

        arguments = [
            (['name'], dict(action='store', help='Application name')),
        ]

    @controller.expose(help='Create new Skyler app')
    def default(self):
        self.log.info('Spinning up stack')
        session = Session()
        app = session.query(Application).filter(Application.name == self.pargs.name).first()
        if not app:
            self.log.error('No application found')
            raise SkylerException("No application found")
        runtime_name = file(os.path.join(app.source, 'runtime.txt')).read().strip()
        rt = getattr(__import__('runtime.{}'.format(runtime_name)), runtime_name)
        runtime = rt.Runtime(app.name)
        runtime.start_deploy()

