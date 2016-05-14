#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

"""
cli for docktree module
"""

from __future__ import print_function
import docktree
import sys
import json
import argparse
try:
    import argcomplete
except ImportError:
    pass


def print_tree(heads, output_format='plain', encoding='ascii'):
    """
    print a tree starting at heads to stdout
    :param heads: heads of the tree
    :param output_format: format of the printed tree, either plain or json
    """
    if output_format == 'plain':
        out = ''
        for head in heads:
            out += _print_tree_wrap(head, encoding=encoding)
        return out
    elif output_format == 'json':
        return json.dumps([dict(layer) for layer in heads])
    else:
        raise ValueError("invalid output_format '{0}'".format(output_format))


def _print_tree_wrap(layer, indentation='', encoding='ascii'):
    """
    wrapper function for recursive implementation of print tree
    :param indentation: indentation for the current layer
    :param encoding: either ascii or utf-8
    :return: the ascii output
    :rtype: str
    """
    new_node = ''

    if layer.parent is None:
        if encoding in 'utf-8':
            new_node += u'\u2500 {lay}\n'.format(lay=str(layer))
        else:
            new_node += '- {lay}\n'.format(lay=str(layer))
    elif layer.parent.children:
        if encoding in 'utf-8':
            new_node += u'{ind}\u2514\u2500 {lay}\n' \
            .format(ind=indentation, lay=str(layer))
        else:
            new_node += '{ind}|- {lay}\n' \
            .format(ind=indentation, lay=str(layer))
    for child in layer.children:
        new_node += _print_tree_wrap(
            layer=child,
            indentation=indentation + '  ',
            encoding=encoding)
    return new_node


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
    parser.add_argument(
        '-f',
        '--format',
        dest='output_format',
        choices=('plain', 'json'),
        default='plain',
        help='the output format'
    )

    if 'argcomplete' in globals().keys():
        argcomplete.autocomplete(parser)

    return parser.parse_args(argv)


def main():
    """
    parse arguments and run the desired action
    """
    args = parse_args()

    layers = docktree.analyze_layers()
    if not args.print_intermediate:
        layers = docktree.remove_untagged_layers(layers)
    heads = docktree.get_heads(layers)

    encoding = sys.getdefaultencoding()
    print(print_tree(heads, output_format=args.output_format, encoding=encoding))

if __name__ == '__main__':
    main()
