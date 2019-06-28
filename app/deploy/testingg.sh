#!/bin/bash

printf "================ TESTING INDEPENDENT START ================\n"

python3 precompute.py 'dataset/ind/product_i_2000_3.csv' 'dataset/ind/customer_i_2000_3.csv' 2
printf "Skenario A done\n"

python3 precompute.py 'dataset/ind/product_i_5000_3.csv' 'dataset/ind/customer_i_5000_3.csv' 2
printf "Skenario B done\n"

printf "================ TESTING ANTI-CORRELATED START ================\n"

python3 precompute.py 'dataset/ant/product_ac_2000_3.csv' 'dataset/ant/customer_ac_2000_3.csv' 2
printf "Skenario A done\n"

python3 precompute.py 'dataset/ant/product_ac_5000_3.csv' 'dataset/ant/customer_ac_5000_3.csv' 2
printf "Skenario B done\n"