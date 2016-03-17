# -*- coding: utf-8 -*-


class ImageLayer(object):
    """
    abstraction of a docker image layer
    """

    def __init__(self, children=None, parent=None, identifier='', tags=None, size=0):
        """
        create and initialize a new ImageLayer object
        :param children: list of children as ImageLayer objects
        :param parent: parent as ImageLayer object
        :param identifier: unique string
        :param tags: list of tags in unicode
        :param size: size of the layer in bytes
        """

        self._children = children if children is not None else []
        self._parent = parent
        self._identifier = identifier
        self._tags = tags if tags is not None else []
        self._size = size

    def __repr__(self):
        """
        :return: string containing a printable representation of a ImageLayer object
        """
        return '{layer_id} Tags: {layer_tag} Size: {layer_size}'.format(
            layer_id=self._identifier[:12],
            layer_tag=str(self._tags),
            layer_size=_convert_size(self.size),
        )

    def print_children(self, indentation=''):
        """
        print a tree following the double-linked list
        :param indentation: indentation for the current layer
        """
        if self.parent is None:
            print('-', self)
        elif len(self.parent.children) >= 1:
            print(indentation, '|-', self)
        for child in self._children:
            child.print_children(indentation + '  ')

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

    @children.deleter
    def children(self):
        """
        delete all children
        """
        del self._children

    def remove_child(self, child):
        """
        remove a specific child from the list of children
        :param child: child to remove
        """
        self._children.remove(child)

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

    @parent.deleter
    def parent(self):
        """
        delete the parent
        """
        del self._parent

    @property
    def identifier(self):
        """
        get the identifier
        :return: identifier of the layer
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        set the identifier
        :param identifier: identifier to set
        """
        self._identifier = identifier

    @identifier.deleter
    def identifier(self):
        """
        delete the identifier
        """
        del self._identifier

    @property
    def tags(self):
        """
        return a list of all tags
        :return: list of tags applied to the image
        :rtype: list
        """
        return self._tags

    @tags.setter
    def tags(self, tag):
        """
        append a tag to the list of all tags
        :param tag: tag to append
        """
        self._tags.append(tag)

    @tags.deleter
    def tags(self):
        """
        delete all tags
        """
        del self._tags

    @property
    def size(self):
        """
        return the size of the layer in bytes
        :return: size of the layer in bytes
        :rtype: int
        """
        return self._size

    @size.deleter
    def size(self):
        """
        delete the size
        """
        del self._size


def _convert_size(size):
    """
    converts size of image to a appropriate printable format
    :param size: size of a image in bytes
    :return: size of a image in appropriate printable format
    :rtype: str
    """
    if size <= 1024:
        return str(size) + ' B'
    elif size <= 1024*1024:
        return str(round(size/1024, 1)) + ' kiB'
    elif size <= 1024*1024*1024:
        return str(round(size/1024/1024, 1)) + ' MiB'
    elif size <= 1024*1024*1024*1024:
        return str(round(size/1024/1024/1024, 1)) + ' GiB'
    else:
        return str(size) + ' B'
