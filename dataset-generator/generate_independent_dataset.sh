#!/bin/bash
MY_DIR='../dataset/independent/'

if [ -d "$MY_DIR" ]; then
  rm -rf ${MY_DIR}*
fi

python3 generate_dataset.py i 10000 3 product
python3 generate_dataset.py i 10000 3 customer
python3 generate_dataset.py i 30000 3 product
python3 generate_dataset.py i 30000 3 customer
python3 generate_dataset.py i 50000 3 product
python3 generate_dataset.py i 50000 3 customer
python3 generate_dataset.py i 70000 3 product
python3 generate_dataset.py i 70000 3 customer
python3 generate_dataset.py i 100000 3 product
python3 generate_dataset.py i 100000 3 customer
