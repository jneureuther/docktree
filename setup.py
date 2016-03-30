#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script
"""

from setuptools import setup
import os
from docktree import __name__ as project_name, __doc__ as description
from docktree import __author__, __email__, __url__


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
    name=project_name,
    version='0.1',
    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    description=description,
    long_description=read('README.rst'),
    url=__url__,
    author=__author__,
    author_email=__email__,
    license=read('LICENSE'),
    packages=[project_name],
    scripts=['bin/{0}'.format(project_name)],
    test_suite="tests",
    install_requires=get_requirements(),
)
