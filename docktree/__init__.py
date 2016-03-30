"""
Analyse dependencies of docker images.
"""

__author__ = 'Julian Neureuther'
__email__ = 'dev@jneureuther.de'
__url__ = 'https://github.com/jneureuther/{0}'.format(__name__)

from .docktree import analyse_layers, get_heads, remove_untagged_layers
