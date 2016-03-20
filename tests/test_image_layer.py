# -*- coding: utf-8 -*-

"""Test the ImageLayer abstraction class"""

import unittest
import string
import random
from .context import ImageLayer


class TestImageLayer(unittest.TestCase):
    """Test the ImageLayer abstraction class"""

    @staticmethod
    def _generate_valid_identifier():
        """generate a random but valid identifier for image layers"""
        allowed_id_chars = list(set(string.hexdigits.lower()))
        return ''.join(
            (random.choice(allowed_id_chars) for i in range(64))
        )

    @staticmethod
    def _generate_tag():
        """generate a random but valid tag for image layers"""
        allowed_tag_chars = string.ascii_letters + string.digits
        return ''.join(
            (random.choice(allowed_tag_chars) for i in range(
                random.randint(1, 100)
            ))
        )

    def test_init_without_id(self):
        """test if identifier is required"""
        self.assertRaises(TypeError, ImageLayer)

    def test_identifier_prop(self):
        """test the identifier property"""
        identifier = TestImageLayer._generate_valid_identifier()
        layer = ImageLayer(identifier)
        self.assertEqual(identifier, layer.identifier)
        # change identifier
        self.assertRaises(
            AttributeError, setattr,
            layer, 'identifier', TestImageLayer._generate_valid_identifier()
        )

    def test_tags_prop(self):
        """test the tags property"""
        identifier = TestImageLayer._generate_valid_identifier()
        tags = [TestImageLayer._generate_tag() for i in range(
            random.randint(0, 50)
        )]
        layer = ImageLayer(identifier, tags=tags)
        self.assertEqual(layer.tags, tags)
        newtag = TestImageLayer._generate_tag()
        tags += newtag
        layer.tags.append(tags)
        self.assertEqual(layer.tags, tags)

    def test_parent_children_prop(self):
        """test the parent and child property"""
        id_child = TestImageLayer._generate_valid_identifier()
        layer_child = ImageLayer(
            identifier=id_child,
            tags=['child'],
            parent=None,
            children=None,
        )
        id_parent = TestImageLayer._generate_valid_identifier()
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
        identifier = TestImageLayer._generate_valid_identifier()
        tags = [TestImageLayer._generate_tag()]
        layer = ImageLayer(identifier, tags=tags)
        self.assertEqual(
            repr(layer),
            "{0} Tags: {1}".format(identifier[:12], tags)
        )

    def test_print_tree(self):
        """test the print_tree function"""
        id_child = TestImageLayer._generate_valid_identifier()
        layer_child = ImageLayer(
            identifier=id_child,
            tags=['child'],
            parent=None,
            children=None,
        )
        id_parent = TestImageLayer._generate_valid_identifier()
        layer_parent = ImageLayer(
            identifier=id_parent,
            tags=['parent'],
            parent=None,
            children=[layer_child],
        )
        layer_child.parent = layer_parent
        self.assertEqual(
            layer_parent.print_tree(),
            "- {id_head} Tags: ['parent']\n"
            "  |- {id_child} Tags: ['child']\n".format(
                id_head=id_parent[:12],
                id_child=id_child[:12],
            )
        )
