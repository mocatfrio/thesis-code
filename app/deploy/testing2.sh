#!/bin/bash

printf "================ TESTING INDEPENDENT START ================\n"

python3 precompute.py 'dataset/ind/product_i_10000_7.csv' 'dataset/ind/customer_i_10000_7.csv' 2
printf "Skenario 5 done\n"

python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 2
printf "Skenario 6 done\n"

python3 precompute.py 'dataset/ind/product_i_50000_3.csv' 'dataset/ind/customer_i_50000_3.csv' 2
printf "Skenario 7 done\n"

python3 precompute.py 'dataset/ind/product_i_100000_3.csv' 'dataset/ind/customer_i_100000_3.csv' 2
printf "Skenario 8 done\n"

python3 precompute.py 'dataset/ind/product_i_200000_3.csv' 'dataset/ind/customer_i_200000_3.csv' 2
printf "Skenario 9 done\n"
