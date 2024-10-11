#!/bin/bash

source ~/miniconda3/etc/profile.d/conda.sh

conda activate exode

source env.sh

python3 -u read_eXode.py
