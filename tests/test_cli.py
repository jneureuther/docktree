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
                self.layers[i].parent = self.layers[j]
                self.layers[j].children.append(self.layers[i])

    def test_json_encoder(self):
        """test the ImageLayerEncoder"""
        testlayer = self.layers[-1]
        json_dump = json.dumps(testlayer, cls=cli.ImageLayerEncoder)
        json_dict = json.loads(json_dump)
        self.assertEqual(json_dict['identifier'], testlayer.identifier)
        for i in range(len(testlayer.children) - 1):
            self.assertEqual(
                json_dict['children'][i]['identifier'],
                testlayer.children[i].identifier
            )
        self.assertEqual(
            json_dict['parent_identifier'],
            testlayer.parent.identifier if testlayer.parent else ''
        )
        self.assertEqual(json_dict['size'], testlayer.size)
        # test if json encoder can encode other objects
        testobject = {'foo': [1, 2, 3], 'bar': {'a': 'b'}, 'baz': 42, }
        json_object = json.loads(
            json.dumps(testobject, cls=cli.ImageLayerEncoder)
        )
        self.assertEqual(testobject, json_object)
