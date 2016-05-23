#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dockgraph: Analyse dependencies of docker images.
# Copyright (C) 2016 Julian Neureuther <dev@jneureuther.de>
#                    sedrubal <dev@sedrubal.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Setup script
"""

from setuptools import setup
import os


def read(fname):
    """returns the text of a file"""
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()


def get_requirements(filename="requirements.txt"):
    """returns a list of all requirements"""
    text = read(filename)
    requirements = []
    for line in text.splitlines():
        req = line.split('#')[0].strip()
        if req != '':
            requirements.append(req)
    return requirements

setup(
    name='dockgraph',
    version='1.0.0',
    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    description='analyse dependencies of docker images',
    long_description=read('README.rst'),
    url='https://github.com/jneureuther/dockgraph',
    author='sedrubal <dev@sedrubal.de>, Julian Neureuther <dev@jneureuther.de>',
    license='GPLv3',
    packages=['dockgraph'],
    scripts=['bin/dockgraph'],
    test_suite="tests",
    install_requires=get_requirements(),
)
