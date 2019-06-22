#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

python3 generate_dataset.py i 20000 3 product
python3 generate_dataset.py i 20000 3 customer
