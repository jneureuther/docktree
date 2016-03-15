#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

"""
Analyse dependencies of docker images.
"""

from __future__ import print_function
from __future__ import absolute_import
from .ImageLayer import ImageLayer

import docker
import sys
import argparse
try:
    import argcomplete
except ImportError:
    pass


def analyse_layers():
    """
    analyse all layers and compute a tree
    :return: dict of images
    :rtype: dict
    """
    docker_cli = docker.Client(base_url='unix://var/run/docker.sock')
    images = docker_cli.images(all=True)

    layers = {}

    for image in images:
        layer = ImageLayer(
            identifier=image['Id'],
            parent_identifier=image['ParentId'],
            tags=image['RepoTags']
        )
        layers[image['Id']] = layer

    for layer in layers.values():
        if layer.parent_identifier != '':
            layers[layer.parent_identifier].children.append(layer)
            layer.parent = layers[layer.parent_identifier]

    return layers


def print_tree(heads):
    """
    print a tree starting at heads to stdout
    :param heads: heads of the tree
    """
    for head in heads:
        head.print_children()


def get_heads(layers):
    """
    return heads of a given tree
    :param layers: double linked list
    :return: heads of the tree
    :rtype: list
    """
    heads = []
    for layer in layers.values():
        if layer.parent_identifier == '':
            heads.append(layer)
    return heads


def remove_untagged_layers(layers):
    """
    remove all untagged layers from the tree
    :param layers: dict containing all layers
    :return: tree without untagged layers
    :rtype: dict
    """
    empty_tags = []

    for layer_id, layer in layers.items():
        if layer.tags[0] == '<none>:<none>':
            empty_tags.append(layer_id)
            if layer.parent is not None:
                layer.parent.remove_child(layer)
                for child in layer.children:
                    layer.parent.children.append(child)
            else:
                for child in layer.children:
                    child.parent_identifier = ''
                    child.parent = None
            if layer.children is not None:
                for child in layer.children:
                    child.parent = layer.parent
                    child.parent_identifier = layer.parent_identifier

    for tag in empty_tags:
        layers.pop(tag)

    return layers


def parse_args(argv=sys.argv[1:]):
    """
    :param argv: arguments which we get called with
    :return: the parsed arguments as object (see argparse doc)
    :rtype: object
    """

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '-i',
        '--intermediate',
        action='store_true',
        dest='print_intermediate',
        default=False,
        help='print intermediate (untagged) layers'
    )

    if 'argcomplete' in globals().keys():
        argcomplete.autocomplete(parser)

    return parser.parse_args(argv)


def main():
    """
    parse arguments and run the desired action
    """
    args = parse_args()

    layers = analyse_layers()
    if not args.print_intermediate:
        layers = remove_untagged_layers(layers)
    heads = get_heads(layers)
    print_tree(heads)

if __name__ == '__main__':
    main()
