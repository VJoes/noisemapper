#!/usr/bin/env python
# -*- coding: utf-8 -*-


from noisemapper import __version__

import os
from setuptools import setup, find_packages
#from distutils.core import setup

readmes = ['README']

readme = ''
for readmef in readmes:
    if os.path.isfile(readmef):
        readme = open(readmef).read()


setup(
    name='NoiseMapper',
    version=__version__,
    author='Paolo De Rosa',
    author_email='paolo.de.rosa@unipi.it',
    url='http://www.dustlab.org/noisemapper/',
    license='MIT',
    description='DustLab Noise Mapper',
    long_description=readme,
    packages=find_packages(),
    platforms=['any'],
    zip_safe=True
)
