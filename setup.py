#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script
"""

from setuptools import setup

with open('README.rst') as f:
    README_FILE = f.read()

with open('LICENSE') as f:
    LICENSE_FILE = f.read()

setup(
    name='docktree',
    version='0.1',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities'
    ],
    description='analyse dependencies of docker images',
    long_description=README_FILE,
    url='https://github.com/jneureuther/docktree',
    author='Julian Neureuther',
    author_email='dev@jneureuther.de',
    license=LICENSE_FILE,
    packages=['docktree'],
    entry_points={
        'console_scripts': [
            'docktree=docktree.docktree:main'
        ]
    },
    install_requires=[
        'argparse',
        'argcomplete>=1.1.0',
        'docker-py>=1.7.2'
    ]
)
