#!/bin/bash

add-apt-repository ppa:deadsnakes/ppa -y
apt update

apt install git
apt install python3.6
apt install python3.6-dev
apt install python-virtualenv
apt install python3-pip
pip3 install --upgrade pip