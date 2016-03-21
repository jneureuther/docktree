docktree
========

.. image:: https://landscape.io/github/jneureuther/docktree/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/jneureuther/docktree/develop
    :alt: Code Health

.. image:: https://codecov.io/github/jneureuther/docktree/coverage.svg?branch=develop
    :target: https://codecov.io/github/jneureuther/docktree?branch=develop

.. image:: https://travis-ci.org/jneureuther/docktree.svg?branch=develop
    :target: https://travis-ci.org/jneureuther/docktree

Analyse dependencies of docker images.

.. code::

  - 65e4158d9625 Tags: ['docker.io/busybox:latest'] Size: 1.1 MiB
     |- 8fa48410182e Tags: ['bar:latest'] Size: 1.1 MiB
       |- 26cc8a5feb49 Tags: ['baz:latest'] Size: 1.1 MiB
     |- 05710237af2f Tags: ['foo:latest'] Size: 1.1 MiB

Usage
-----

command-line
~~~~~~~~~~~~

.. code:: bash

  usage: docktree-cli [-h] [-i]

  cli for docktree module

  optional arguments:
    -h, --help          show this help message and exit
    -i, --intermediate  print intermediate (untagged) layers

module
~~~~~~

.. code:: python

  import docktree
  help(docktree.docktree)

Contributing
------------

| If you have Vagrant_ installed, just run ``vagrant up`` in order
| to spin up a virtual machine containing everything needed for development.
| Docktree will be installed system-wide and a set of example data is generated.
|
| To copy new code into the vm run:

.. code:: bash

  vagrant rsync
  sudo bash -c "cd /vagrant/ && python3 setup.py develop && cd -"

.. _Vagrant: https://www.vagrantup.com/

unittests
~~~~~~~~~

Provide unittests_ whenever you can. Run them by executing:

.. _unittests: tests/

.. code:: bash

  ./setup.py test

License
-------

Attribution-ShareAlike 4.0 International
