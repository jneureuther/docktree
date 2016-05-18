# -*- coding: utf-8 -*-

"""Test the argparse parsers in cli"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from dockgraph import dockgraph_cli as cli


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
