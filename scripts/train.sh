#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Training models...
python3.6 ./src/trainer.py  $1
./scripts/evaluate.sh

echo Copying model to download folder...
curr=$(pwd)
cd ./src/nlp/models
cp ../../../download/models.tar.gz ../../../download/models_temp.tar.gz
tar -zcvf ../../../download/models.tar.gz .
cd $pwd

deactivate