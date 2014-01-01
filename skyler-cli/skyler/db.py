import datetime
from cement.core import controller
from sqlalchemy import create_engine, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:////var/lib/skyler/database.sqlite')  # TODO: replace with openstack mysql
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    source = Column(String)  # for now - just directory name
    runtime = Column(String)
    history = relationship("Deployment")
    network_id = Column(String, nullable=True, default=None)



DEPLOYMENT_STATE_STARTED, DEPLOYMENT_STATE_BUILT_OK, DEPLOYMENT_STATE_SUCCESSFUL = range(3)
DEPLOYMENT_STATE_READABLE = {DEPLOYMENT_STATE_STARTED: 'started',
                             DEPLOYMENT_STATE_BUILT_OK: 'built',
                             DEPLOYMENT_STATE_SUCCESSFUL: 'successful'}


class Deployment(Base):
    __tablename__ = 'deployments_history'

    id = Column(Integer, primary_key=True)
    application = relationship("Application")
    application_id = Column(Integer, ForeignKey('applications.id'))
    image = Column(String)
    stack_name = Column(String)
    created = Column(DateTime, default=datetime.datetime.now)
    state = Column(Integer)


class InitDBController(controller.CementBaseController):
    class Meta:
        label = 'init'
        description = 'init database'
        config_defaults = dict()
        arguments = []

    @controller.expose()
    def default(self):
        self.log.info('Initializing database...')
        Base.metadata.create_all(engine)

