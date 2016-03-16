docktree
========

.. image:: https://landscape.io/github/jneureuther/docktree/develop/landscape.svg?style=flat
   :target: https://landscape.io/github/jneureuther/docktree/develop
   :alt: Code Health

Analyse dependencies of docker images.

.. code::

  - 65e4158d9625 Tags: ['docker.io/busybox:latest']
     |- d4b4a1f6de61 Tags: ['bar:latest']
       |- 29f89a1915a8 Tags: ['baz:latest']
     |- ab8665c3e355 Tags: ['foo:latest']

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
  sudo bash -c "cd /vagrant/ && ./setup.py develop && cd -"

.. _Vagrant: https://www.vagrantup.com/

License
-------

Attribution-ShareAlike 4.0 International