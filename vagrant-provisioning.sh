#!/bin/bash

set -e

sudo su

echo -e "\n==== updating all packages ===="
dnf -y upgrade

echo -e "\n==== installing dependencies ===="
dnf -y install docker vim python3-ipython

echo -e "\n==== start docker and add user vagrant to docker group"
systemctl start docker
getent group docker || groupadd docker
gpasswd -a vagrant docker
systemctl restart docker

echo -e "\n==== generate test data ===="
docker pull busybox
docker run --name foo busybox touch foo
docker commit foo foo
docker rm foo
docker run --name bar busybox touch bar
docker commit bar bar
docker rm bar
docker run --name baz bar touch baz
docker commit baz baz
docker rm baz

echo -e "\n==== install dockgraph ===="
cd /vagrant && python3 setup.py develop && cd -
activate-global-python-argcomplete
