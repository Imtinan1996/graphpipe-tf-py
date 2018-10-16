# Copyright (c) 2018, Oracle and/or its affiliates. All rights reserved.
#
# Licensed under the Universal Permissive License v 1.0 as shown at
# http://oss.oracle.com/licenses/upl.

import subprocess

import setuptools

from codecs import open
from os import path



class BinaryDistribution(setuptools.Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(self):
        return True


subprocess.call(['make', '-C', 'remote_op'])

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

requirements = None
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='graphpipe_tf',
    version='1.0.4',
    description='Graphpipe helpers for TensorFlow remote ops',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='OCI ML Team',
    install_requires=requirements,
    author_email='vish.ishaya@oracle.com',
    url='https://oracle.github.io/graphpipe',
    classifier=[
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: Universal Permissive License (UPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=['graphpipe_tf'],
    package_data={'graphpipe_tf': ['remote_op.so']},
    distclass=BinaryDistribution,
)
