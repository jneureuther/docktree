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
    :param encoding: the terminal encoding (ascii or utf-8)
    """
    if output_format == 'plain':
        out = ''
        headstr = u'\u2500' if encoding == 'utf-8' else '-'
        chldstr = u'\u2514\u2500' if encoding == 'utf-8' else '|-'
        for head in heads:
            out += _print_tree_wrap(head, headstr=headstr, chldstr=chldstr)
        return out
    elif output_format == 'json':
        return json.dumps([dict(layer) for layer in heads])
    else:
        raise ValueError("invalid output_format '{0}'".format(output_format))


def _print_tree_wrap(layer, indentation='', headstr='-', chldstr='|-'):
    """
    wrapper function for recursive implementation of print tree
    :param indentation: indentation for the current layer
    :param headstr: the string to be used in front of heads
    :param chldstr: the string to be used in front of childs
    :return: the text output
    :rtype: str
    """
    new_node = ''

    if layer.parent is None:
        new_node += u'{headstr} {lay}\n'.format(
            headstr=headstr, lay=str(layer))
    elif layer.parent.children:
        new_node += u'{ind}{chldstr} {lay}\n'.format(
            ind=indentation, chldstr=chldstr, lay=str(layer))
    for child in layer.children:
        new_node += _print_tree_wrap(
            layer=child,
            indentation=indentation + '  ',
            headstr=headstr,
            chldstr=chldstr,
        )
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
