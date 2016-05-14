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


def generate_random_layer(max_tag_count=2):
    """
    :return: a layer with random tags and id
    :param max_tag_count: the maximum count of tags the layer should have
    """
    return ImageLayer(
        identifier=generate_valid_identifier(),
        tags=[generate_tag() for _ in range(random.randint(0, max_tag_count))],
        size=random.randint(0, 1024*1024*1024)
    )


def connect_layers_random(layers_list):
    """
    connects some layers in list layers_list randomly to a tree
    by using join_parent_child
    :param layers_list: a list of ImageLayer instances
    """
    for i, layer in enumerate(layers_list[:-1]):
        ImageLayer.join_parent_child(
            parent=random.choice(layers_list[i+1:]),
            child=layer
        )


class TestCli(unittest.TestCase):
    """Test the cli script"""

    def setUp(self):
        """generate some ImageLayers"""
        self.layers = [generate_random_layer() for _ in range(10)]
        # connect parent and child
        connect_layers_random(self.layers)
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
        for i, layer in enumerate(self.heads):
            self.assertDictEqual(json_heads[i], dict(layer))

    def test_print_tree_default(self):
        """test if the default output_format of print_tree is plain"""
        text = cli.print_tree(self.heads, output_format='plain')
        text_default = cli.print_tree(self.heads)
        self.assertEqual(text, text_default)

    def test_print_tree_plain_ascii(self):
        """test the print_tree function with plain as output_format and ascii"""
        text = cli.print_tree(
            self.heads,
            output_format='plain',
            encoding='ascii'
        )
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
        for i, layer in enumerate(self.heads):
            self.assertEqual(
                text_heads[i].identifier,
                layer.identifier[:12]
            )
            self.assertListEqual(text_heads[i].tags, layer.tags)
            self.assertEqual(
                _convert_size(text_heads[i].size),
                _convert_size(layer.size)
            )
            self.assertEqual(
                len(text_heads[i].children),
                len(layer.children)
            )
            self.assertTrue(text_heads[i].is_head())

    def test_print_tree_plain_utf8(self):
        """test the print_tree function with plain as output_format and utf-8"""
        text = cli.print_tree(
            self.heads,
            output_format='plain',
            encoding='utf-8'
        )
        line_regex = re.compile(
            r"(?P<indent> {0,}\u2514?\u2500 )"
            r"(?P<id>[0-9a-f]{12})"
            r" Tags: (?P<tags>\[(\'[a-zA-Z0-9:\./]{1,}\'(, )?){0,}\])"
            r" Size: (?P<size>\d{1,}(\.\d)? ([KMGT]i)?B)",
            re.UNICODE
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
            if indent == '─ ':
                text_heads.append(layer)
            elif indent == '  └─ ':
                ImageLayer.join_parent_child(
                    parent=text_heads[-1],
                    child=layer,
                )
            # else: we're only testing the heads and their children
            # (not the childs of childs)
        for i, layer in enumerate(self.heads):
            self.assertEqual(
                text_heads[i].identifier,
                layer.identifier[:12]
            )
            self.assertListEqual(text_heads[i].tags, layer.tags)
            self.assertEqual(
                _convert_size(text_heads[i].size),
                _convert_size(layer.size)
            )
            self.assertEqual(
                len(text_heads[i].children),
                len(layer.children)
            )
            self.assertTrue(text_heads[i].is_head())
