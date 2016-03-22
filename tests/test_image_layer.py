# -*- coding: utf-8 -*-

"""Test the ImageLayer abstraction class"""

import unittest
import string
import random
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from docktree.ImageLayer import ImageLayer
from docktree.ImageLayer import _convert_size


def _generate_valid_identifier():
    """:return a random but valid identifier for image layers"""
    allowed_id_chars = list(set(string.hexdigits.lower()))
    return ''.join(
        (random.choice(allowed_id_chars) for i in range(64))
    )


def _generate_tag():
    """:return a random but valid tag for image layers"""
    allowed_tag_chars = string.ascii_letters + string.digits
    return ''.join(
        (random.choice(allowed_tag_chars) for i in range(
            random.randint(1, 100)
        ))
    )


class TestImageLayer(unittest.TestCase):
    """Test the ImageLayer abstraction class"""

    def test_init_without_id(self):
        """test if identifier is required"""
        self.assertRaises(TypeError, ImageLayer)

    def test_identifier_prop(self):
        """test the identifier property"""
        identifier = _generate_valid_identifier()
        layer = ImageLayer(identifier)
        self.assertEqual(identifier, layer.identifier)
        # change identifier
        self.assertRaises(
            AttributeError, setattr,
            layer, 'identifier', _generate_valid_identifier()
        )

    def test_tags_prop(self):
        """test the tags property"""
        identifier = _generate_valid_identifier()
        tags = [_generate_tag() for i in range(random.randint(0, 50))]
        layer = ImageLayer(identifier, tags=tags)
        self.assertEqual(layer.tags, tags)
        newtag = _generate_tag()
        tags += newtag
        layer.tags.append(tags)
        self.assertEqual(layer.tags, tags)

    def test_size_prop(self):
        """test the tags property"""
        identifier = _generate_valid_identifier()
        size = random.randint(0, 9999999999999)
        layer = ImageLayer(identifier, size=size)
        self.assertEqual(layer.size, size)
        # change size
        self.assertRaises(
            AttributeError, setattr,
            layer, 'size', random.randint(0, 9999999999999)
        )

    def test_parent_children_prop(self):
        """test the parent and child property"""
        id_child = _generate_valid_identifier()
        layer_child = ImageLayer(
            identifier=id_child,
            tags=['child'],
            parent=None,
            children=None,
        )
        id_parent = _generate_valid_identifier()
        layer_parent = ImageLayer(
            identifier=id_parent,
            tags=['parent'],
            parent=None,
            children=[layer_child],
        )
        self.assertEqual(layer_parent.children[0], layer_child)
        layer_child.parent = layer_parent
        self.assertEqual(layer_child.parent, layer_parent)
        layer_child.parent = None
        self.assertIsNone(layer_child.parent)
        layer_parent.remove_child(layer_child)
        self.assertEqual(layer_parent.children, [])

    def test_repr(self):
        """test the __repr__ function"""
        identifier = _generate_valid_identifier()
        tags = [_generate_tag()]
        size = random.randint(0, 9999999999999)
        size_human = _convert_size(size)
        layer = ImageLayer(identifier, tags=tags, size=size)
        self.assertEqual(
            repr(layer),
            "{0} Tags: {1} Size: {2}".format(identifier[:12], tags, size_human)
        )

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

    def test_print_tree(self):
        """test the print_tree function"""
        id_child = _generate_valid_identifier()
        size_child = 42*1024*1024*1024
        layer_child = ImageLayer(
            identifier=id_child,
            tags=['child'],
            parent=None,
            children=None,
            size=size_child,
        )
        id_parent = _generate_valid_identifier()
        size_parent = 10*1024*1024
        layer_parent = ImageLayer(
            identifier=id_parent,
            tags=['parent'],
            parent=None,
            children=[layer_child],
            size=size_parent,
        )
        layer_child.parent = layer_parent
        self.assertEqual(
            layer_parent.print_tree(),
            "- {id_head} Tags: ['parent'] Size: {size_head}\n"
            "  |- {id_child} Tags: ['child'] Size: {size_child}\n".format(
                id_head=id_parent[:12],
                id_child=id_child[:12],
                size_head=_convert_size(size_parent),
                size_child=_convert_size(size_child),
            )
        )
