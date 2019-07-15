#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

# python3 generate_dataset.py i 500 3 product
# python3 generate_dataset.py i 500 3 customer
# python3 generate_dataset.py i 1000 3 product
# python3 generate_dataset.py i 1000 3 customer
# python3 generate_dataset.py i 10000 3 product
# python3 generate_dataset.py i 10000 3 customer
python3 generate_dataset.py i 5000 4 product
python3 generate_dataset.py i 5000 4 customer
python3 generate_dataset.py i 5000 5 product
python3 generate_dataset.py i 5000 5 customer
python3 generate_dataset.py i 5000 6 product
python3 generate_dataset.py i 5000 6 customer
python3 generate_dataset.py i 5000 7 product
python3 generate_dataset.py i 5000 7 customer