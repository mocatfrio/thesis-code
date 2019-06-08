#!/bin/bash
MY_DIR='../dataset/anti_correlated/'

if [ -d "$MY_DIR" ]; then
  rm -rf ${MY_DIR}*
fi

python3 generate_dataset.py ac 10000 3 product
python3 generate_dataset.py ac 10000 3 customer
python3 generate_dataset.py ac 30000 3 product
python3 generate_dataset.py ac 30000 3 customer
python3 generate_dataset.py ac 50000 3 product
python3 generate_dataset.py ac 50000 3 customer
python3 generate_dataset.py ac 70000 3 product
python3 generate_dataset.py ac 70000 3 customer
python3 generate_dataset.py ac 100000 3 product
python3 generate_dataset.py ac 100000 3 customer