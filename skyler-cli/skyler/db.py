from cement.core import controller
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////var/lib/skyler/database.sqlite')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    source = Column(String)  # for now - just directory name


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

