#!/usr/bin/env python

from distutils.core import setup
from glob import glob
from os.path import splitext, basename

from setuptools import find_packages

setup(name='activity-rest-api',
      version='1.0',
      description='Python REST Api',
      author='Mia Frank',
      packages=find_packages('activity-tracker'),
      package_dir={'': 'activity-tracker'},
      py_modules=[splitext(basename(path))[0] for path in glob('activity-tracker/*.py')], install_requires=['boto3',
                                                                                                            'flask',
                                                                                                            'requests',
                                                                                                            'moto'
                                                                                                            ]
      )
