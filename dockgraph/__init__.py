"""
analyse dependencies of docker images
"""

from .dockgraph import analyze_layers, get_heads, remove_untagged_layers

__version__ = '1.0.0'
__url__ = 'https://github.com/jneureuther/dockgraph'
__author__ = 'Julian Neureuther <dev@jneureuther.de>, \
              sedrubal <dev@sedrubal.de>'
__copyright__ = 'Copyright (C) 2016 The authors of dockgraph'
__license__ = 'GPLv3'
