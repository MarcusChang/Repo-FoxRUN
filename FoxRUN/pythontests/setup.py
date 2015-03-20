#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import shutil
from subprocess import Popen, PIPE
#from distutils.sysconfig import get_python_lib
from setuptools import setup, find_packages

# dependencies
with open('requirements.txt') as f:
    deps = f.read().splitlines()

version = "0.0.1"

# main setup script
setup(
    name="webapptest",
    version=version,
    packages=find_packages(),
    description="webapp test",
    author="marcus_chang",
    install_requires=deps,

    package_data={'': ['mtbf/mtbf_config.json','mtbf/mtbf.list', 'endurance/manifest.ini',  'ui/manifest.ini',  'testvars.json']},
    include_package_data=True
)
