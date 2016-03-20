#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Test the argparse parsers in cli"""

import unittest
from .context import docktree_cli as cli


class TestRequirementsParser(unittest.TestCase):
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
        self.assertEqual('ascii', args.output_format)
        args = cli.parse_args('--format ascii'.split(' '))
        self.assertEqual('ascii', args.output_format)
        args = cli.parse_args('--format json'.split(' '))
        self.assertEqual('json', args.output_format)

if __name__ == '__main__':
    unittest.main()
