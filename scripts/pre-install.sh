#!/bin/bash

apt update

add-apt-repository ppa:deadsnakes/ppa
apt update

apt install git
apt install python3.6
apt install python3-dev
apt install python-virtualenv
apt install python3-pip