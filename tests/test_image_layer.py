# -*- coding: utf-8 -*-

"""Test the ImageLayer abstraction class"""

import unittest
import random
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from tests.helper import generate_valid_identifier, generate_tag

from dockgraph.ImageLayer import ImageLayer
from dockgraph.ImageLayer import _convert_size

__author__ = 'Julian Neureuther <dev@jneureuther.de>, \
              sedrubal <dev@sedrubal.de>'
__copyright__ = 'Copyright (C) 2016 The authors of dockgraph'
__license__ = 'GPLv3'


class TestImageLayer(unittest.TestCase):
    """Test the ImageLayer abstraction class"""

    def test_init_without_id(self):
        """test if identifier is required"""
        self.assertRaises(TypeError, ImageLayer)

    def test_identifier_prop(self):
        """test the identifier property"""
        identifier = generate_valid_identifier()
        layer = ImageLayer(identifier)
        self.assertEqual(identifier, layer.identifier)
        # change identifier
        self.assertRaises(
            AttributeError, setattr,
            layer, 'identifier', generate_valid_identifier()
        )

    def test_tags_prop(self):
        """test the tags property"""
        identifier = generate_valid_identifier()
        tags = [generate_tag() for _ in range(random.randint(0, 50))]
        layer = ImageLayer(identifier, tags=tags)
        self.assertListEqual(layer.tags, tags)
        newtag = generate_tag()
        tags += newtag
        layer.tags.append(tags)
        self.assertListEqual(layer.tags, tags)
        tags = [generate_tag() for _ in range(2)]
        layer.tags = tags
        self.assertListEqual(layer.tags, tags)

    def test_size_prop(self):
        """test the tags property"""
        identifier = generate_valid_identifier()
        size = random.randint(0, 9999999999999)
        layer = ImageLayer(identifier, size=size)
        self.assertEqual(layer.size, size)
        # change size
        self.assertRaises(
            AttributeError, setattr,
            layer, 'size', random.randint(0, 9999999999999)
        )

    def test_join_parent_child(self):
        """test the join_parent_child function to build the tree"""
        id_head = generate_valid_identifier()
        layer_head = ImageLayer(
            identifier=id_head,
            tags=['head'],
        )
        id_middle = generate_valid_identifier()
        layer_middle = ImageLayer(
            identifier=id_middle,
            tags=['middle'],
        )
        id_middle2 = generate_valid_identifier()
        layer_middle2 = ImageLayer(
            identifier=id_middle2,
            tags=['middle2'],
        )
        id_child = generate_valid_identifier()
        layer_child = ImageLayer(
            identifier=id_child,
            tags=['child'],
        )
        self.assertIsNone(layer_head.parent)
        self.assertIsNone(layer_middle.parent)
        self.assertIsNone(layer_middle2.parent)
        self.assertIsNone(layer_child.parent)
        self.assertEqual(len(layer_head.children), 0)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        # join head and middle
        ImageLayer.join_parent_child(parent=layer_head, child=layer_middle)
        self.assertIsNone(layer_head.parent)
        self.assertEqual(layer_middle.parent, layer_head)
        self.assertIsNone(layer_middle2.parent)
        self.assertIsNone(layer_child.parent)
        self.assertEqual(len(layer_head.children), 1)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        self.assertEqual(layer_head.children[0], layer_middle)
        # join head and middle2
        ImageLayer.join_parent_child(parent=layer_head, child=layer_middle2)
        self.assertIsNone(layer_head.parent)
        self.assertEqual(layer_middle.parent, layer_head)
        self.assertEqual(layer_middle2.parent, layer_head)
        self.assertIsNone(layer_child.parent)
        self.assertEqual(len(layer_head.children), 2)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        self.assertEqual(layer_head.children[0], layer_middle)
        self.assertEqual(layer_head.children[1], layer_middle2)
        # join middle and child
        ImageLayer.join_parent_child(parent=layer_middle, child=layer_child)
        self.assertIsNone(layer_head.parent)
        self.assertEqual(layer_middle.parent, layer_head)
        self.assertEqual(layer_middle2.parent, layer_head)
        self.assertEqual(layer_child.parent, layer_middle)
        self.assertEqual(len(layer_head.children), 2)
        self.assertEqual(len(layer_middle.children), 1)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        self.assertEqual(layer_head.children[0], layer_middle)
        self.assertEqual(layer_head.children[1], layer_middle2)
        self.assertEqual(layer_middle.children[0], layer_child)

    def test_remove_from_chain(self):
        """Test the remove_from_chain function to reduce the tree"""
        id_head = generate_valid_identifier()
        layer_head = ImageLayer(
            identifier=id_head,
            tags=['head'],
        )
        id_middle = generate_valid_identifier()
        layer_middle = ImageLayer(
            identifier=id_middle,
            tags=['middle'],
        )
        id_middle2 = generate_valid_identifier()
        layer_middle2 = ImageLayer(
            identifier=id_middle2,
            tags=['middle2'],
        )
        id_child = generate_valid_identifier()
        layer_child = ImageLayer(
            identifier=id_child,
            tags=['child'],
        )
        # build tree
        ImageLayer.join_parent_child(parent=layer_head, child=layer_middle)
        ImageLayer.join_parent_child(parent=layer_head, child=layer_middle2)
        ImageLayer.join_parent_child(parent=layer_middle, child=layer_child)
        # remove middle2 from chain
        layer_middle2.remove_from_chain()
        self.assertIsNone(layer_head.parent)
        self.assertEqual(layer_middle.parent, layer_head)
        self.assertIsNone(layer_middle2.parent)
        self.assertEqual(layer_child.parent, layer_middle)
        self.assertEqual(len(layer_head.children), 1)
        self.assertEqual(len(layer_middle.children), 1)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        self.assertEqual(layer_head.children[0], layer_middle)
        self.assertEqual(layer_middle.children[0], layer_child)
        # remove middle from chain
        layer_middle.remove_from_chain()
        self.assertIsNone(layer_head.parent)
        self.assertIsNone(layer_middle.parent)
        self.assertIsNone(layer_middle2.parent)
        self.assertEqual(layer_child.parent, layer_head)
        self.assertEqual(len(layer_head.children), 1)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        # remove head from chain
        layer_head.remove_from_chain()
        self.assertIsNone(layer_head.parent)
        self.assertIsNone(layer_middle.parent)
        self.assertIsNone(layer_middle2.parent)
        self.assertIsNone(layer_child.parent)
        self.assertEqual(len(layer_head.children), 0)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)

    def test_str(self):
        """test the __str__ function"""
        identifier = generate_valid_identifier()
        tags = [generate_tag()]
        size = random.randint(0, 9999999999999)
        size_human = _convert_size(size)
        layer = ImageLayer(identifier, tags=tags, size=size)
        self.assertEqual(
            str(layer),
            "{0} Tags: {1} Size: {2}".format(identifier[:12], tags, size_human)
        )

    def test_iter(self):
        """test the __iter__ function"""
        layer_parent = ImageLayer(
            identifier=generate_valid_identifier(),
            tags=[generate_tag() for _ in range(random.randint(0, 5))],
            size=random.randint(0, 1024*1024*1024*1024)
        )
        layer_child = ImageLayer(
            identifier=generate_valid_identifier(),
            tags=[generate_tag() for _ in range(random.randint(0, 5))],
            size=random.randint(0, 1024*1024*1024*1024)
        )
        ImageLayer.join_parent_child(
            parent=layer_parent,
            child=layer_child,
        )
        dict_parent = dict(layer_parent)
        dict_child = dict(layer_child)
        self.assertEqual(dict_parent['Id'], layer_parent.identifier)
        self.assertEqual(dict_parent['ParentId'], '')
        self.assertListEqual(dict_parent['RepoTags'], layer_parent.tags)
        self.assertEqual(dict_parent['VirtualSize'], layer_parent.size)
        self.assertListEqual(dict_parent['Children'], [dict(layer_child)])
        self.assertEqual(dict_child['Id'], layer_child.identifier)
        self.assertEqual(dict_child['ParentId'], layer_parent.identifier)
        self.assertListEqual(dict_child['RepoTags'], layer_child.tags)
        self.assertEqual(dict_child['VirtualSize'], layer_child.size)
        self.assertListEqual(dict_child['Children'], [])

    def test_convert_size(self):
        """test the size to human conversation"""
        self.assertEqual(_convert_size(0), '0 B')
        self.assertEqual(_convert_size(1), '1 B')
        self.assertEqual(_convert_size(1023), '1023 B')
        self.assertEqual(_convert_size(1024), '1.0 KiB')
        self.assertEqual(_convert_size(1023*1024), '1023.0 KiB')
        self.assertEqual(_convert_size(1024*1024), '1.0 MiB')
        self.assertEqual(_convert_size(1023*1024*1024), '1023.0 MiB')
        self.assertEqual(_convert_size(1024*1024*1024), '1.0 GiB')
        self.assertEqual(_convert_size(1023*1024*1024*1024), '1023.0 GiB')
        self.assertEqual(_convert_size(1024*1024*1024*1024), '1.0 TiB')
        self.assertEqual(_convert_size(1023*1024*1024*1024*1024), '1023.0 TiB')
