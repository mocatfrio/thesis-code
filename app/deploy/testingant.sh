#!/bin/bash

printf "================ TESTING ANTI-CORRELATED START ================\n"

python3 precompute.py 'dataset/ant/product_ac_50000_3.csv' 'dataset/ant/customer_ac_50000_3.csv' 2
printf "Skenario 7 done\n"

python3 precompute.py 'dataset/ant/product_ac_100000_3.csv' 'dataset/ant/customer_ac_100000_3.csv' 2
printf "Skenario 8 done\n"

python3 precompute.py 'dataset/ant/product_ac_200000_3.csv' 'dataset/ant/customer_ac_200000_3.csv' 2
printf "Skenario 9 done\n"
