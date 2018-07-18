#!/bin/bash

set -e
if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

if ! [ -x "$(command -v apt)" ]; then
  echo "Right now only Debian is supported and 'apt' has to be installed"
  exit 1
fi

INSTALL=""
if ! [ -x "$(command -v python3)" ]; then
  INSTALL="$INSTALL python3"
fi
if ! [ -x "$(command -v pip3)" ]; then
  INSTALL="$INSTALL python3-pip"
fi
if [ ! -f /usr/share/doc/apt-transport-https/copyright ]; then
  INSTALL="$INSTALL apt-transport-https"
fi
if ! [ -x "$(command -v curl)" ]; then
	INSTALL="$INSTALL curl"
fi
if [ ! -f /etc/default/nfs-common ]; then
  INSTALL="$INSTALL nfs-common"
fi
if ! [ -x "$(command -v gocryptfs)" ]; then
  INSTALL="$INSTALL gocryptfs"
fi
if ! [ -x "$(command -v fusermount)" ]; then
  INSTALL="$INSTALL fusermount"
fi

# setup syncthing install
if ! [ -x "$(command -v syncthing)" ]; then
	echo "> adding syncthing to syncthing.list"
	curl -s https://syncthing.net/release-key.txt | apt-key add -
	echo "deb https://apt.syncthing.net/ syncthing stable" | tee /etc/apt/sources.list.d/syncthing.list
  apt update -yqq
  apt install -yqq syncthing
fi
