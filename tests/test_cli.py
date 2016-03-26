# -*- coding: utf-8 -*-

"""Test the cli script"""

import unittest
import sys
import os
import random
import json
import re

sys.path.insert(0, os.path.abspath('.'))

from tests.test_image_layer import generate_valid_identifier, generate_tag
from bin import docktree_cli as cli
from docktree.ImageLayer import ImageLayer
from docktree.ImageLayer import _convert_size


def generate_random_layer():
    """generates a layer with random tags and id"""
    return ImageLayer(
        identifier=generate_valid_identifier(),
        tags=[generate_tag() for _ in range(random.randint(0, 2))],
        size=random.randint(0, 1024*1024*1024)
    )


class TestCli(unittest.TestCase):
    """Test the cli script"""

    def setUp(self):
        """generate some ImageLayers"""
        self.layers = [generate_random_layer() for _ in range(10)]
        # connect parent and child
        for i in range(len(self.layers) - 1):
            j = random.randint(i, len(self.layers) - 1)
            if i != j:
                ImageLayer.join_parent_child(
                    parent=self.layers[j],
                    child=self.layers[i],
                )
        self.heads = [layer for layer in self.layers if layer.parent is None]

    def test_print_tree_invalid(self):
        """test the print_tree function with an invalid output_format"""
        self.assertRaises(
            ValueError, cli.print_tree, self.heads, output_format='foobar')

    def test_print_tree_json(self):
        """test the print_tree function with json as output_format"""
        text = cli.print_tree(self.heads, output_format='json')
        json_heads = json.loads(text)
        self.assertEqual(len(json_heads), len(self.heads))
        for i in range(len(self.heads)):
            self.assertEqual(json_heads[i], dict(self.heads[i]))

    def test_print_tree_default(self):
        """test if the default output_format of print_tree is ascii"""
        text = cli.print_tree(self.heads, output_format='ascii')
        text_default = cli.print_tree(self.heads)
        self.assertEqual(text, text_default)

    def test_print_tree_ascii(self):
        """test the print_tree function with ascii as output_format"""
        text = cli.print_tree(self.heads, output_format='ascii')
        line_regex = re.compile(
            r"(?P<indent> {0,}\|?- )"
            r"(?P<id>[0-9a-f]{12})"
            r" Tags: (?P<tags>\[(\'[a-zA-Z0-9:\./]{1,}\'(, )?){0,}\])"
            r" Size: (?P<size>\d{1,}(\.\d)? ([KMGT]i)?B)"
        )
        text_heads = []
        for line in text.splitlines():
            matches = line_regex.match(line)
            self.assertIsNotNone(matches)
            indent = matches.group('indent')
            identifier = matches.group('id')
            size_str = matches.group('size')
            size = float(size_str.split(' ')[0])
            convert = {'B': 0, 'KiB': 1, 'MiB': 2, 'GiB': 3, 'TiB': 4}
            size *= 1024**convert[size_str.split(' ')[1]]
            tags = json.loads(matches.group('tags').replace("'", '"'))
            self.assertIsInstance(tags, list)
            layer = ImageLayer(
                identifier=identifier,
                tags=tags,
                size=size,
            )
            if indent == '- ':
                text_heads.append(layer)
            elif indent == '  |- ':
                ImageLayer.join_parent_child(
                    parent=text_heads[-1],
                    child=layer,
                )
            # else: we're only testing the heads and their children
            # (not the childs of childs)
        for i in range(len(self.heads)):
            self.assertEqual(
                text_heads[i].identifier,
                self.heads[i].identifier[:12]
            )
            self.assertEqual(text_heads[i].tags, self.heads[i].tags)
            self.assertEqual(
                _convert_size(text_heads[i].size),
                _convert_size(self.heads[i].size)
            )
            self.assertEqual(
                len(text_heads[i].children),
                len(self.heads[i].children)
            )
            if self.heads[i].parent:
                self.assertEqual(
                    text_heads[i].parent.identifier,
                    self.heads[i].parent.identifier
                )
            else:
                self.assertIsNone(text_heads[i].parent)
