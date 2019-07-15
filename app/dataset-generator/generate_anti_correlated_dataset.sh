#!/bacn/bash
# MY_DIR='../dataset/anti_correlated/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

# python3 generate_dataset.py ac 500 3 product
# python3 generate_dataset.py ac 500 3 customer
# python3 generate_dataset.py ac 1000 3 product
# python3 generate_dataset.py ac 1000 3 customer
# python3 generate_dataset.py ac 10000 3 product
# python3 generate_dataset.py ac 10000 3 customer
python3 generate_dataset.py ac 5000 4 product
python3 generate_dataset.py ac 5000 4 customer
python3 generate_dataset.py ac 5000 5 product
python3 generate_dataset.py ac 5000 5 customer
python3 generate_dataset.py ac 5000 6 product
python3 generate_dataset.py ac 5000 6 customer
python3 generate_dataset.py ac 5000 7 product
python3 generate_dataset.py ac 5000 7 customer
