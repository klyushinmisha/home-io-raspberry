#!/bin/bash

pip3 install -r requirements.txt

if [ "$(uname)" == "Darwin" ]; then
    brew install redis      
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    apt-get update
    apt-get install -y redis
