# -*- coding: utf-8 -*-

"""
Tools to make a tree data structure for Docker layers
"""


class ImageLayer(object):
    """
    abstraction of a docker image layer
    """

    def __init__(self, identifier, tags=None, size=0):
        """
        create and initialize a new ImageLayer object
        :param identifier: unique string
        :param children: list of children as ImageLayer objects
        :param parent: parent as ImageLayer object
        :param tags: list of tags in unicode
        :param size: size of the layer in bytes
        """

        self._identifier = identifier
        self._tags = tags if tags is not None else []
        self._size = size
        self._parent = None
        self._children = []

    def __str__(self):
        """
        :return: a printable description of an ImageLayer object as string
        """
        return u'{layer_id} Tags: {layer_tag} Size: {layer_size}'.format(
            layer_id=self._identifier[:12],
            layer_tag=str(self._tags),
            layer_size=_convert_size(self.size),
        )

    def __iter__(self):
        """makes ImageLayer object iterable (e.g. for dict(layer))"""
        yield('Id', self.identifier)
        yield('ParentId', self.parent.identifier if self.parent else '')
        yield('RepoTags', self.tags)
        yield('VirtualSize', self.size)
        yield('Children', [dict(child) for child in self.children])

    @staticmethod
    def join_parent_child(parent, child):
        """add child to the parent's childs and set child.parent to parent"""
        parent.children.append(child)
        child.parent = parent

    def remove_from_chain(self):
        """
        removes the layer from the double linked list.
        It appends all children to it's parent and
        sets the new parent of all children
        """
        for child in self.children:
            child.parent = self.parent
            if not self.is_head():
                self.parent.children.append(child)
        self.children = []
        if not self.is_head():
            self.parent.children.remove(self)
            self.parent = None

    def is_head(self):
        """
        :return True if this layer is a head / if this layer has no parent
        """
        return self.parent is None

    @property
    def children(self):
        """
        :return: list of all children
        :rtype: list
        """
        return self._children

    @children.setter
    def children(self, children):
        """
        add a list of children
        :param children: children to append
        """
        self._children = children

    @property
    def parent(self):
        """
        get the parent object
        :return: parent object
        :rtype: object
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        set the parent
        :param parent: parent object
        """
        self._parent = parent

    @property
    def identifier(self):
        """
        get the identifier
        :return: identifier of the layer
        :rtype: str
        """
        return self._identifier

    @property
    def tags(self):
        """
        return a list of all tags
        :return: list of tags applied to the image
        :rtype: list
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        set the tags for this layer
        :param tags: tags for the layer
        """
        self._tags = tags

    @property
    def size(self):
        """
        return the size of the layer in bytes
        :return: size of the layer in bytes
        :rtype: int
        """
        return self._size


def _convert_size(size):
    """
    converts size of image to a human readable format (base is 1024)
    :param size: size of a image in bytes
    :return: size of a image in human readable format
    :rtype: str
    """
    if size >= 1024*1024*1024*1024:
        return '{0:.1f} TiB'.format(size/1024/1024/1024/1024)
    elif size >= 1024*1024*1024:
        return '{0:.1f} GiB'.format(size/1024/1024/1024)
    elif size >= 1024*1024:
        return '{0:.1f} MiB'.format(size/1024/1024)
    elif size >= 1024:
        return '{0:.1f} KiB'.format(size/1024)
    else:
        return '{0} B'.format(size)
