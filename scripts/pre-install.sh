#!/bin/bash

add-apt-repository ppa:deadsnakes/ppa -y
apt update

apt install -y git
apt install -y python3.6
apt install -y python3.6-dev
apt install -y python-virtualenv
apt install -y python3-pip
pip3 install --upgrade pip