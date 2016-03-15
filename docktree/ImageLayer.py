# -*- coding: utf-8 -*-


class ImageLayer(object):
    """
    A Docker layer for object orientated algorythms
    """
    def __init__(self, children=None, parent=None, identifier='', parent_identifier='', tags=None):
        """
        create and initialize a new ImageLayer object
        :param children: list of children as ImageLayer objects
        :param parent: parent as ImageLayer object
        :param identifier: unique string
        :param parent_identifier: unique identifier of parent layer
        :param tags: list of tags in unicode
        """

        self._children = children if children is not None else []
        self._parent = parent
        self._identifier = identifier
        self._parent_identifier = parent_identifier
        self._tags = tags if tags is not None else []

    def __repr__(self):
        """
        :return: string containing a printable representation of a ImageLayer object
        """
        return self._identifier[:12] + ' Tags: ' + str(self._tags)

    def print_children(self, indentation=''):
        """
        print a tree following the double-linked list
        :param indentation: indentation for the current layer
        """
        if self._parent_identifier == '':
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
    def parent_identifier(self):
        """
        get the identifier of the parent layer
        :return: identifier of the parent layer
        :rtype: str
        """
        return self._parent_identifier

    @parent_identifier.setter
    def parent_identifier(self, parent_identifier):
        """
        set the identifier of the parent layer
        :param parent_identifier: identifier of the parent layer
        """
        self._parent_identifier = parent_identifier

    @parent_identifier.deleter
    def parent_identifier(self):
        """
        delete the identifier of the parent layer
        """
        del self._parent_identifier

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
