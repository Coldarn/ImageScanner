#!/usr/bin/env python

import os
from setuptools import setup, find_packages

REQUIREMENTS = [
    'python-cjson', 
    'autoconnect', 
    'importlib',
    'PIL',
]

# Required only by Posix:
if os.name == 'posix': REQUIREMENTS.append('pysane')

setup(name='imagescanner',
      version='0.9-alpha',
      description='Multi-platform Python library to access scanner devices.',
      author='Sergio Oliveira',
      author_email='seocam@seocam.com',
      url='http://code.google.com/p/imagescanner/',
      packages=find_packages(),
      package_data={'': ['*.tiff']},
      install_requires=REQUIREMENTS,
     )

