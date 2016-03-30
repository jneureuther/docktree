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


def generate_random_api_layer(max_tag_count=2):
    """
    :return: a dict containing a layer like it's provided by docker api
    :param max_tag_count: the maximum count of tags the layer should have
    """
    repo_digests = []
    tags = [generate_tag() for _ in range(max_tag_count)]
    if not tags:
        tags.append('<none>:<none>')
        repo_digests.append('<none>@<none>')
    return {
        'Created': random.randint(0, 3000000000),
        'Id': generate_valid_identifier(),
        'ParentId': '',
        'Labels': {},
        'RepoTags': tags,
        'RepoDigests': repo_digests,
        'Size': 0,
        'VirtualSize': random.randint(0, 1024*1024*1024*1024),
    }


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

    def test_analyze_layers(self):
        """docstring for test_analyze_layers"""
        api_list = [generate_random_api_layer() for _ in range(15)]
        # connect parent and child
        for i, api_layer in enumerate(api_list[:-1]):
            api_layer['ParentId'] = random.choice(api_list[i+1:])['Id']
        analyzed_dict = docktree.analyze_layers(api_list)
        # check for consistency (key is identifier of value)
        for identifier, layer in analyzed_dict.items():
            self.assertEqual(layer.identifier, identifier)
        # check if all layers from api are in the dict
        self.assertEqual(len(analyzed_dict), len(api_list))
        for api_layer in api_list:
            self.assertIn(api_layer['Id'], analyzed_dict.keys())
            analyzed_layer = analyzed_dict[api_layer['Id']]
            self.assertEqual(analyzed_layer.size, api_layer['VirtualSize'])
            if api_layer['ParentId']:
                self.assertIsNotNone(
                    analyzed_layer.parent,
                    "Parent should not be None. There was a ParentId in API"
                )
                self.assertEqual(
                    analyzed_layer.parent.identifier,
                    api_layer['ParentId']
                )
                self.assertIn(
                    analyzed_layer,
                    analyzed_layer.parent.children,
                    "The current layer should be in parent's children list"
                )
                for child in analyzed_layer.children:
                    self.assertEqual(child.parent, analyzed_layer)
            else:
                self.assertIsNone(
                    analyzed_layer.parent,
                    "Parent should be None. There was no ParentId in API"
                )

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
            self.assertEqual(layer.identifier, identifier)
        for identifier, layer in tagged_layers.items():
            self.assertEqual(layer.identifier, identifier)
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
