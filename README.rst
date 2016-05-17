dockgraph
=========

.. image:: https://www.quantifiedcode.com/api/v1/project/32fe64b69f144531a2ed7c908aca46a8/badge.svg
    :target: https://www.quantifiedcode.com/app/project/32fe64b69f144531a2ed7c908aca46a8
    :alt: Code issues

.. image:: https://landscape.io/github/jneureuther/docktree/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/jneureuther/docktree/develop
    :alt: Code Health

.. image:: https://coveralls.io/repos/github/jneureuther/docktree/badge.svg?branch=develop
    :target: https://coveralls.io/github/jneureuther/docktree?branch=develop

.. image:: https://travis-ci.org/jneureuther/docktree.svg?branch=develop
    :target: https://travis-ci.org/jneureuther/docktree

.. image:: https://readthedocs.org/projects/docktree/badge/?version=latest
    :target: http://docktree.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

Analyse dependencies of docker images.

.. code::

  ─── 307ac631f1b5 Tags: ['docker.io/busybox:latest'] Size: 1.1 MiB
      ├── b6fd900f4d6a Tags: ['bar:latest'] Size: 1.1 MiB
      │   └── 700decaa0660 Tags: ['baz:latest'] Size: 1.1 MiB
      └── 5731cad94676 Tags: ['foo:latest'] Size: 1.1 MiB

  1 heads, 4 layers

Usage
-----

You can find the latest documentation on https://docktree.rtfd.org/.

command-line
~~~~~~~~~~~~

.. code:: bash

  usage: dockgraph [-h] [-i] [-f {text,json}] [-e {ascii,utf-8}]
                  [images [images ...]]

  cli for dockgraph module

  positional arguments:
    images                image(s) to print, either specified by
                          [repository]:[tag] or by the (abbreviated) image id

  optional arguments:
    -h, --help            show this help message and exit
    -i, --intermediate    print intermediate (untagged) layers
    -f {text,json}, --format {text,json}
                          the output format
    -e {ascii,utf-8}, --encoding {ascii,utf-8}
                          the output encoding

module
~~~~~~

.. code:: python

  import dockgraph
  help(dockgraph.dockgraph)

Contributing
------------

You are very welcome to contribute to this project either by a pull request or
by filing an issue/feature-request!

Vagrant
~~~~~~~

| If you have Vagrant_ installed, just run ``vagrant up`` in order
| to spin up a virtual machine containing everything needed for development.
| Dockgraph will be installed system-wide and a set of example data is generated.
|
| In order to automatically copy modified code into the vm run:

.. code:: bash

  vagrant rsync-auto

.. _Vagrant: https://www.vagrantup.com/

Virtual Environment
~~~~~~~~~~~~~~~~~~~

If you have docker installed on your local machine you could also work in a
`virtual environment`_:

.. code:: bash

  pip3 install virtualenv
  virtualenv .env
  source .env/bin/activate
  ./setup.py develop

.. _`virtual environment`: http://docs.python-guide.org/en/latest/dev/virtualenvs/

unittests
~~~~~~~~~

Provide unittests_ whenever you can.
 - Name them ``test_foobar.py``.
 - Run them by executing:

.. _unittests: tests/

.. code:: bash

  ./setup.py test
  # or
  coverage3 run setup.py test && coverage3 html
  # in order to generate a code coverage report

License
-------

`Creative Commons Attribution-ShareAlike 4.0
<LICENSE>`_
