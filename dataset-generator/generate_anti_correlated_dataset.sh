#!/bin/bash
# MY_DIR='../dataset/anti_correlated/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi
python3 generate_dataset.py ac 2000 3 product
python3 generate_dataset.py ac 2000 3 customer
python3 generate_dataset.py ac 3000 3 product
python3 generate_dataset.py ac 3000 3 customer
python3 generate_dataset.py ac 4000 3 product
python3 generate_dataset.py ac 4000 3 customer