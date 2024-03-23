#!/usr/bin/env python

from setuptools import setup
from pywpcare import get_version

setup(
  name='pywpcare',
  version=get_version(),
  description='Python classes to manage WPCare datamodel',
  author='vanGamo',
  author_email='vangamo.beta@gmail.com',
  packages=['pywpcare'],  # same as name
  install_requires=['wheel', 'psycopg2-binary']
  )