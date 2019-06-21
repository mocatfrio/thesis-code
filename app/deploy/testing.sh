#!/bin/bash

python3 precompute.py 'dataset/ind/product_i_10000_3.csv' 'dataset/ind/customer_i_10000_3.csv' 1
python3 precompute.py 'dataset/ind/product_i_10000_3.csv' 'dataset/ind/customer_i_10000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_10000_3.csv' 'dataset/ind/customer_i_10000_3.csv' 3
printf "skenario 1 done\n"

python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 1
python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 3
printf "skenario 2 done\n"

python3 precompute.py 'dataset/ind/product_i_50000_3.csv' 'dataset/ind/customer_i_50000_3.csv' 1
python3 precompute.py 'dataset/ind/product_i_50000_3.csv' 'dataset/ind/customer_i_50000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_50000_3.csv' 'dataset/ind/customer_i_50000_3.csv' 3
printf "skenario 3 done\n"

python3 precompute.py 'dataset/ind/product_i_100000_3.csv' 'dataset/ind/customer_i_100000_3.csv' 1
python3 precompute.py 'dataset/ind/product_i_100000_3.csv' 'dataset/ind/customer_i_100000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_100000_3.csv' 'dataset/ind/customer_i_100000_3.csv' 3
printf "skenario 4 done\n"

python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 1
python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 3
printf "skenario 5 done\n"