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


class Deployment(Base):
    __tablename__ = 'deployments_history'

    id = Column(Integer, primary_key=True)
    application = relationship("Application")
    application_id = Column(Integer, ForeignKey('applications.id'))
    image = Column(String)
    created = Column(DateTime, default=datetime.datetime.now)


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

