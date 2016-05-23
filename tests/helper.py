# -*- coding: utf-8 -*-

# dockgraph: Analyse dependencies of docker images.
# Copyright (C) 2016 Julian Neureuther <dev@jneureuther.de>
#                    sedrubal <dev@sedrubal.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Helper for tests"""

import random
import string

from dockgraph.ImageLayer import ImageLayer


def generate_valid_identifier():
    """:return a random but valid identifier for image layers"""
    allowed_id_chars = list(set(string.hexdigits.lower()))
    return ''.join(
        (random.choice(allowed_id_chars) for _ in range(64))
    )


def generate_tag():
    """:return a random but valid tag for image layers"""
    allowed_tag_chars = string.ascii_letters + string.digits
    return ''.join(
        (random.choice(allowed_tag_chars) for _ in range(
            random.randint(1, 100)
        ))
    )


def generate_random_api_layer(max_tag_count=2):
    """
    :return: a dict containing a layer like it's provided by docker api
    :param max_tag_count: the maximum count of tags the layer should have
    """
    repo_digests = []
    tags = [generate_tag() for _ in range(random.randint(0, max_tag_count))]
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


def generate_random_layer(max_tag_count=2):
    """
    :return: a layer with random tags and id
    :param max_tag_count: the maximum count of tags the layer should have
    """
    return ImageLayer(
        identifier=generate_valid_identifier(),
        tags=[generate_tag() for _ in range(random.randint(0, max_tag_count))],
        size=random.randint(0, 1024*1024*1024)
    )


def connect_layers_random(layers_list):
    """
    connects some layers in list layers_list randomly to a tree
    by using join_parent_child
    :param layers_list: a list of ImageLayer instances
    """
    for i, layer in enumerate(layers_list[:-1]):
        ImageLayer.join_parent_child(
            parent=random.choice(layers_list[i+1:]),
            child=layer
        )
