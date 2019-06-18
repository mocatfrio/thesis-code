#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

python3 generate_dataset.py i 2000 3 product
python3 generate_dataset.py i 2000 3 customer
python3 generate_dataset.py i 3000 3 product
python3 generate_dataset.py i 3000 3 customer
python3 generate_dataset.py i 4000 3 product
python3 generate_dataset.py i 4000 3 customer