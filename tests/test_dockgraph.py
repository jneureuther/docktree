# -*- coding: utf-8 -*-

"""Test the dockgraph.dockgraph module"""

import unittest
import random
import os
import sys
from copy import deepcopy

sys.path.insert(0, os.path.abspath('.'))

from tests.helper import generate_random_api_layer
from tests.helper import generate_random_layer
from tests.helper import connect_layers_random

from dockgraph import dockgraph
from dockgraph.ImageLayer import ImageLayer

__author__ = 'Julian Neureuther <dev@jneureuther.de>, \
              sedrubal <dev@sedrubal.de>'
__copyright__ = 'Copyright (C) 2016 The authors of dockgraph'
__license__ = 'GPLv3'


class Testdockgraph(unittest.TestCase):
    """Test the dockgraph.dockgraph module"""

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
        self.static_layers = {
            'ezue4PoF7Im1zae2kie9uokua3ze3dae8ode9edooPhah7Eifaekae' +
            'F9aith1EeX':
            ImageLayer(
                identifier='ezue4PoF7Im1zae2kie9uokua3ze3dae8ode9ed' +
                'ooPhah7EifaekaeF9aith1EeX',
                tags=['foo1/bar:baz'],
                size=1
            ),
            'xielael0biezoreire7ieth9teeKohphoh2Cheew8uoreeYoosa1ja' +
            'tha2eejeic':
            ImageLayer(
                identifier='xielael0biezoreire7ieth9teeKohphoh2Chee' +
                'w8uoreeYoosa1jatha2eejeic',
                tags=['foo2/bar:baz'],
                size=2
            ),
            'zoomee1eiNgieF8ees0Eemieruaneeyee9so5na8ahdo0chaizahth' +
            'ahph7eekub':
            ImageLayer(
                identifier='zoomee1eiNgieF8ees0Eemieruaneeyee9so5na' +
                '8ahdo0chaizahthahph7eekub',
                tags=['foo3/bar:baz'],
                size=3
            )
        }
        self.static_layers['ezue4PoF7Im1zae2kie9uokua3ze3dae8ode9ed' +
                           'ooPhah7EifaekaeF9aith1EeX'].parent = \
            self.static_layers['xielael0biezoreire7ieth9teeKohphoh2Chee' +
                               'w8uoreeYoosa1jatha2eejeic']
        self.static_layers['xielael0biezoreire7ieth9teeKohphoh2Chee' +
                           'w8uoreeYoosa1jatha2eejeic'].parent = \
            self.static_layers['zoomee1eiNgieF8ees0Eemieruaneeyee9so5na' +
                               '8ahdo0chaizahthahph7eekub']
        self.static_heads = [
            self.static_layers['zoomee1eiNgieF8ees0Eemieruaneeyee9so5na' +
                               '8ahdo0chaizahthahph7eekub']
        ]

    def test_analyze_layers(self):
        """docstring for test_analyze_layers"""
        api_list = [generate_random_api_layer() for _ in range(15)]
        # connect parent and child
        for i, api_layer in enumerate(api_list[:-1]):
            api_layer['ParentId'] = random.choice(api_list[i+1:])['Id']
        analyzed_dict = dockgraph.analyze_layers(api_list)
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

    def test_get_all_heads(self):
        """test the get_heads method returns a list of heads"""
        heads = dockgraph.get_heads(self.layers)
        self.assertListEqual(heads, self.heads)
        for layer in heads:
            self.assertTrue(layer.is_head())

    def test_get_heads_for_id(self):
        """test the get_heads function with a given id"""
        heads = dockgraph.get_heads(self.static_layers, 'ezue4PoF7Im')
        self.assertListEqual(heads, self.static_heads)
        for layer in heads:
            self.assertTrue(layer.is_head())

    def test_get_heads_for_name(self):
        """test the get_heads function with a given name"""
        heads = dockgraph.get_heads(self.static_layers, 'foo1/bar:baz')
        self.assertListEqual(heads, self.static_heads)
        for layer in heads:
            self.assertTrue(layer.is_head())

    def test_get_heads_for_head(self):
        """test the get_heads function with a head element"""
        heads = dockgraph.get_heads(self.static_layers, 'foo3/bar:baz')
        self.assertListEqual(heads, self.static_heads)
        for layer in heads:
            self.assertTrue(layer.is_head())

    def test_remove_untagged_layers(self):
        """test the remove_untagged_layers function"""
        test_layers = deepcopy(self.layers)
        tagged_layers = dockgraph.remove_untagged_layers(test_layers)
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
