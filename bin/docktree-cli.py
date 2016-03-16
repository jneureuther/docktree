#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

"""
cli for docktree module
"""

import docktree
import sys
import argparse
try:
    import argcomplete
except ImportError:
    pass


def print_tree(heads):
    """
    print a tree starting at heads to stdout
    :param heads: heads of the tree
    """
    for head in heads:
        head.print_children()


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

    layers = docktree.analyse_layers()
    if not args.print_intermediate:
        layers = docktree.remove_untagged_layers(layers)
    heads = docktree.get_heads(layers)
    print_tree(heads)

if __name__ == '__main__':
    main()
