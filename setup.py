#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='imagescanner',
      version='0.8.2',
      description='Multi-platform Python library to access scanner devices.',
      author='Sergio Campos',
      author_email='seocam@seocam.net',
      url='http://code.google.com/p/imagescanner/',
      packages=find_packages(),
      package_data={'': ['*.tiff']},
      install_requires=[],
     )

