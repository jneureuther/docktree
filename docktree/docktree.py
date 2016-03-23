# -*- coding: utf-8 -*-

"""
Analyse dependencies of docker images.
"""

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
            tags=[tag for tag in image['RepoTags'] if tag != '<none>:<none>'],
            size=image['VirtualSize'],
        )
        layers[image['Id']] = layer

    for image in images:
        if image['ParentId'] != '':
            ImageLayer.join_parent_child(
                parent=layers[image['ParentId']],
                child=layers[image['Id']],
            )

    return layers


def get_heads(layers):
    """
    return heads of a given tree
    :param layers: double linked list
    :return: heads of the tree
    :rtype: list
    """
    return [layer for layer in layers.values() if layer.is_head()]


def remove_untagged_layers(layers):
    """
    remove all untagged layers from the tree
    :param layers: dict containing all layers
    :return: tree without untagged layers
    :rtype: dict
    """
    for layer_id, layer in layers.items():
        if not layer.tags:
            layer.remove_from_chain()
            layers.pop(layer_id)

    return layers
