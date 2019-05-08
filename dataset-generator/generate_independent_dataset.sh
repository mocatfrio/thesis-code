#!/bin/bash
MY_DIR='../dataset/independent/'

if [ -d "$MY_DIR" ]; then
  rm -rf ${MY_DIR}*
fi

python3 generate_dataset.py i 100 2 product
python3 generate_dataset.py i 100 2 customer
python3 generate_dataset.py i 500 2 product
python3 generate_dataset.py i 500 2 customer
