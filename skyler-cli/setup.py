#!/usr/bin/env python

from setuptools import setup

setup(name='skyler-cli',
      version='1.0',
      description='Skyler CLI',
      author='Roman Rader',
      author_email='roman.rader@gmail.com',
      url='https://github.com/antigluk/skyler',
      packages=['skyler'],
      install_requires=['cement==2.0.2',
                        'SQLAlchemy==0.8.4',
                        'texttable==0.8.1',
      ],
      entry_points={
          'console_scripts': [
              'skyler = skyler.skyler:main',
              'test = skyler.test:main',
          ]
      }
)
