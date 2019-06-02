#!/bin/bash

version=`git describe --tags --abbrev=0`
echo "Downloading models for version ${version}..."
wget "https://github.com/AmeyKamat/MEERA/releases/download/${version}/models.tar.gz" -P download