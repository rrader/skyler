from cement.core import controller
from db import Application, Session
from texttable import Texttable


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
