docktree
========

.. image:: https://www.quantifiedcode.com/api/v1/project/32fe64b69f144531a2ed7c908aca46a8/badge.svg
  :target: https://www.quantifiedcode.com/app/project/32fe64b69f144531a2ed7c908aca46a8
  :alt: Code issues

.. image:: https://landscape.io/github/jneureuther/docktree/develop/landscape.svg?style=flat
   :target: https://landscape.io/github/jneureuther/docktree/develop
   :alt: Code Health

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

  usage: docktree-cli [-h] [-i] [--format {ascii,json}]

  cli for docktree module

  optional arguments:
    -h, --help            show this help message and exit
    -i, --intermediate    print intermediate (untagged) layers
    --format {ascii,json}
                          the output format

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

License
-------

Attribution-ShareAlike 4.0 International
