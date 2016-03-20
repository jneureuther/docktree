# -*- coding: utf-8 -*-


class ImageLayer(object):
    """
    abstraction of a docker image layer
    """

    def __init__(self, identifier, children=None, parent=None, tags=None):
        """
        create and initialize a new ImageLayer object
        :param identifier: unique string
        :param children: list of children as ImageLayer objects
        :param parent: parent as ImageLayer object
        :param tags: list of tags in unicode
        """

        self._identifier = identifier
        self._children = children if children is not None else []
        self._parent = parent
        self._tags = tags if tags is not None else []

    def __repr__(self):
        """
        :return: string containing a printable representation of a ImageLayer object
        """
        return '{0} Tags: {1}'.format(self._identifier[:12], str(self._tags))

    def print_children(self, indentation=''):
        """
        print a tree following the double-linked list
        :param indentation: indentation for the current layer
        :return: the ascii output
        :rtype: str
        """
        output = ''
        if self.parent is None:
            output += '- {lay}\n'.format(lay=self)
        elif len(self.parent.children) >= 1:
            output += '{ind}|- {lay}\n'.format(ind=indentation, lay=self)
        for child in self._children:
            output += child.print_children(indentation + '  ')
        return output

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
