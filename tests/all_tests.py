#!/usr/bin/env python

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
Run all unittests
"""

import sys
import os
import unittest


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
