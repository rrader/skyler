#!/usr/bin/env python

from setuptools import setup

setup(name='skyler-cli',
      version='1.0',
      description='Skyler CLI',
      author='Roman Rader',
      author_email='roman.rader@gmail.com',
      url='https://github.com/antigluk/skyler',
      packages=['skyler', 'skyler.runtime', 'skyler.clients'],
      install_requires=['cement==2.0.2',
                        'SQLAlchemy>=0.8.4',
                        'texttable>=0.8.1',
                        'python-heatclient>=0.2.6',
                        'python-keystoneclient>=0.4.1',
                        'python-neutronclient>=2.3.2',
                        'docker-py>=0.2.3',
                        'six>=1.4.0',
                        'netaddr>=0.7.10'
      ],
      dependency_links=[
                        'git+git://github.com/dotcloud/docker-py.git#egg=docker-py',
      ],
      entry_points={
          'console_scripts': [
              'skyler = skyler.skyler:main',
          ]
      }
)
