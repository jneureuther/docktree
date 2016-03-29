# -*- coding: utf-8 -*-

"""Test the docktree.docktree module"""

import unittest
import os
import sys
import random

sys.path.insert(0, os.path.abspath('.'))

from tests.test_cli import generate_random_layer

from docktree.ImageLayer import ImageLayer
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
        for i in range(len(self.layers) - 1):
            j = random.randint(i, len(self.layers) - 1)
            if i != j:
                ImageLayer.join_parent_child(
                    parent=list(self.layers.values())[j],
                    child=list(self.layers.values())[i],
                )
        # example implementation of get_heads
        self.heads = [lay for lay in self.layers.values() if lay.is_head()]

    def test_get_heads(self):
        """test the get_heads method returns a list of heads"""
        heads = docktree.get_heads(self.layers)
        self.assertEqual(len(heads), len(self.heads))
        for layer in heads:
            self.assertTrue(layer in self.heads)
