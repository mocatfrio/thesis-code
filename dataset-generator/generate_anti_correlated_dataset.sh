#!/bin/bash
MY_DIR='../dataset/anti_correlated/'

if [ -d "$MY_DIR" ]; then
  rm -rf ${MY_DIR}*
fi

python3 generate_dataset.py ac 100 4 product
python3 generate_dataset.py ac 100 4 customer
python3 generate_dataset.py ac 500 2 product
python3 generate_dataset.py ac 500 2 customer
