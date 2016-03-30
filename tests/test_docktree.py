# -*- coding: utf-8 -*-

"""Test the docktree.docktree module"""

import unittest
import os
import sys
import random
from copy import deepcopy

sys.path.insert(0, os.path.abspath('.'))

from tests.test_cli import generate_random_layer, connect_layers_random
from tests.test_image_layer import generate_valid_identifier, generate_tag

from docktree import docktree


class TestDocktree(unittest.TestCase):
    """Test the docktree.docktree module"""

    def setUp(self):
        """generate some ImageLayers"""
        self.layers = {}
        for _ in range(10):
            layer = generate_random_layer(max_tag_count=random.randint(0, 2))
            self.layers[layer.identifier] = layer
        # connect parent and child
        connect_layers_random(list(self.layers.values()))
        # example implementation of get_heads
        self.heads = [lay for lay in self.layers.values() if lay.is_head()]

    def test_get_heads(self):
        """test the get_heads method returns a list of heads"""
        heads = docktree.get_heads(self.layers)
        self.assertListEqual(heads, self.heads)
        for layer in heads:
            self.assertTrue(layer.is_head())

    def test_remove_untagged_layers(self):
        """test the remove_untagged_layers function"""
        test_layers = deepcopy(self.layers)
        tagged_layers = docktree.remove_untagged_layers(test_layers)
        # check for consistency (key is identifier of value)
        for identifier, layer in test_layers.items():
            self.assertEqual(test_layers[identifier].identifier, identifier)
        for identifier, layer in tagged_layers.items():
            self.assertEqual(tagged_layers[identifier].identifier, identifier)
        # check if test_layers has changed (when copy() is missing)
        for identifier, layer in self.layers.items():
            self.assertDictEqual(dict(layer), dict(test_layers[identifier]))
        # check if items in tagged_layers have the same values for their
        # properties as in test_layers
        for identifier, layer in tagged_layers.items():
            self.assertEqual(
                layer.identifier,
                test_layers[identifier].identifier
            )
            self.assertEqual(
                layer.size,
                test_layers[identifier].size
            )
            self.assertListEqual(
                layer.tags,
                test_layers[identifier].tags
            )
        # check if every layer with tags is in tagged_layers and no layer
        # without tags is in tagged_layers
        for identifier, layer in self.layers.items():
            if layer.tags:
                self.assertIn(identifier, tagged_layers.keys())
                cur = layer.parent
                while cur is not None and not cur.tags:
                    cur = cur.parent
                if cur is None:
                    self.assertIsNone(tagged_layers[identifier].parent)
                else:
                    self.assertEqual(
                        tagged_layers[identifier].parent.identifier,
                        cur.identifier,
                    )
            else:
                self.assertNotIn(identifier, tagged_layers.keys())
