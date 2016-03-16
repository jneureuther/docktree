# -*- coding: utf-8 -*-

"""
Analyse dependencies of docker images.
"""

from __future__ import print_function
from __future__ import absolute_import
from .ImageLayer import ImageLayer

import docker


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
            tags=image['RepoTags']
        )
        layers[image['Id']] = layer

    for image in images:
        if image['ParentId'] != '':
            layers[image['ParentId']].children.append(layers[image['Id']])
            layers[image['Id']].parent = layers[image['ParentId']]

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
        if layer.parent is None:
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
                    child.parent = None
            if layer.children is not None:
                for child in layer.children:
                    child.parent = layer.parent

    for tag in empty_tags:
        layers.pop(tag)

    return layers
