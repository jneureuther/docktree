#!/usr/bin/env python

"""
Run all unittests
"""

import sys
import os
import unittest

__author__ = 'Julian Neureuther <dev@jneureuther.de>, \
              sedrubal <dev@sedrubal.de>'
__copyright__ = 'Copyright (C) 2016 The authors of dockgraph'
__license__ = 'GPLv3'


TESTDIR = os.path.dirname(__file__)


def _is_valid_testcase(filename):
    """:return True if filename is a valid filename for a testcase"""
    return os.path.isfile(os.path.join(TESTDIR, filename)) and \
        filename.startswith('test_') and \
        filename.endswith('.py')


def main():
    """run all unittests and exit with 0 if it was successful"""
    testmodules = [
        f.split('.')[0] for f in os.listdir(TESTDIR) if _is_valid_testcase(f)
    ]
    tests = unittest.TestLoader().loadTestsFromNames(testmodules)

    result = unittest.TextTestRunner(verbosity=1).run(tests)
    sys.exit(not result.wasSuccessful())


if __name__ == '__main__':
    main()
