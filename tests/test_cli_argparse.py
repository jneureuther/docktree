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

"""Test the argparse parsers in cli"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from bin import dockgraph_cli as cli


class TestCliArgParse(unittest.TestCase):
    """Test the argparse parsers in cli"""

    def test_intermediate(self):
        """test if intermediate switch is parsed correctly"""
        args = cli.parse_args([])
        self.assertEqual(False, args.print_intermediate)
        args = cli.parse_args('-i'.split(' '))
        self.assertEqual(True, args.print_intermediate)
        args = cli.parse_args('--inter'.split(' '))
        self.assertEqual(True, args.print_intermediate)
        args = cli.parse_args('--intermediate'.split(' '))
        self.assertEqual(True, args.print_intermediate)

    def test_format(self):
        """test if all formats are parsed correctly"""
        args = cli.parse_args([])
        self.assertEqual('text', args.output_format)
        args = cli.parse_args('-f text'.split(' '))
        self.assertEqual('text', args.output_format)
        args = cli.parse_args('--fo text'.split(' '))
        self.assertEqual('text', args.output_format)
        args = cli.parse_args('--format text'.split(' '))
        self.assertEqual('text', args.output_format)
        args = cli.parse_args('-f json'.split(' '))
        self.assertEqual('json', args.output_format)
        args = cli.parse_args('--for json'.split(' '))
        self.assertEqual('json', args.output_format)
        args = cli.parse_args('--format json'.split(' '))
        self.assertEqual('json', args.output_format)

    def test_encoding(self):
        """test if all encodings are parsed correctly"""
        args = cli.parse_args([])
        self.assertEqual(sys.stdout.encoding, args.output_encoding)
        args = cli.parse_args('-e ascii'.split(' '))
        self.assertEqual('ascii', args.output_encoding)
        args = cli.parse_args('--en ascii'.split(' '))
        self.assertEqual('ascii', args.output_encoding)
        args = cli.parse_args('--encoding ascii'.split(' '))
        self.assertEqual('ascii', args.output_encoding)
        args = cli.parse_args('-e utf-8'.split(' '))
        self.assertEqual('utf-8', args.output_encoding)
        args = cli.parse_args('--enc utf-8'.split(' '))
        self.assertEqual('utf-8', args.output_encoding)
        args = cli.parse_args('--encoding utf-8'.split(' '))
        self.assertEqual('utf-8', args.output_encoding)
