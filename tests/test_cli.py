# -*- coding: utf-8 -*-

"""Test the cli script"""

import unittest
import sys
import os
import random
import json

sys.path.insert(0, os.path.abspath('.'))

from tests.test_image_layer import generate_valid_identifier, generate_tag
from bin import docktree_cli as cli
from docktree.ImageLayer import ImageLayer


def generate_random_layer():
    """generates a layer with random tags and id"""
    return ImageLayer(
        identifier=generate_valid_identifier(),
        tags=[generate_tag() for _ in range(random.randint(0, 2))],
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
