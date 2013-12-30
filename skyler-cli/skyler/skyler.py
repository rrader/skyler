#!/usr/bin/env python
from application import ApplicationListController, ApplicationCreationController

from cement.core import foundation, controller, handler
from db import InitDBController


class SkylerBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = 'Skyler CLI: PaaS on OpenStack'

    @controller.expose(hide=True)
    def default(self):
        self.app.args.print_help()


class Skyler(foundation.CementApp):
    class Meta:
        label = 'skyler-cli'
        base_controller = SkylerBaseController


def main():
    app = Skyler('skyler-cli')
    handler.register(ApplicationListController)
    handler.register(ApplicationCreationController)
    handler.register(InitDBController)
    try:
        app.setup()
        app.run()
    finally:
        app.close()


if __name__ == "__main__":
    main()
