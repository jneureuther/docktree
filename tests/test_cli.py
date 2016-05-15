# -*- coding: utf-8 -*-

"""Test the cli script"""

import unittest
import sys
import os
import json
import re

sys.path.insert(0, os.path.abspath('.'))

from tests.helper import generate_random_api_layer
from tests.helper import generate_random_layer
from tests.helper import connect_layers_random

from bin import docktree_cli as cli
from docktree.ImageLayer import ImageLayer
from docktree.ImageLayer import _convert_size


class TestCli(unittest.TestCase):
    """Test the cli script"""

    def setUp(self):
        """generate some ImageLayers"""
        self.layers = [generate_random_layer() for _ in range(10)]
        # connect parent and child
        connect_layers_random(self.layers)
        self.heads = [layer for layer in self.layers if layer.parent is None]

    def test_image_completer(self):
        """test the argcompletion for docker images"""
        api_list = [generate_random_api_layer() for _ in range(15)]
        suggestions = cli.image_completer('', docker_images=api_list)
        self.assertIn(api_list[0]['Id'][:12], suggestions)
        api_image_tag = None
        for api_image in api_list:
            if api_image['RepoTags']:
                api_image_tag = api_image['RepoTags'][0]
        if not api_image_tag:
            return
        self.assertIn(api_image_tag, suggestions)
        suggestions = cli.image_completer(api_image_tag[0],
                                          docker_images=api_list)
        self.assertIn(api_image_tag, suggestions)
        suggestions = cli.image_completer(api_image_tag,
                                          docker_images=api_list)
        self.assertIn(api_image_tag, suggestions)

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
