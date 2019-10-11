#!/bin/bash

redis-server --daemonize yes
python3 master.py
