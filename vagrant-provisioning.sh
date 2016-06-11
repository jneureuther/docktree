#!/bin/bash

# dockgraph: Analyse dependencies of docker images.
# Copyright (C) 2016 Julian Neureuther <dev@jneureuther.de>
#                    sedrubal <dev@sedrubal.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
