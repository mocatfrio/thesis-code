#!/bin/bash

printf "================ TESTING FOREST-COVER START ================\n"

python3 precompute.py 'dataset/fc/product_fc_10000_6.csv' 'dataset/fc/customer_fc_10000_6.csv' 2
printf "Skenario 4 done\n"

python3 precompute.py 'dataset/fc/product_fc_10000_7.csv' 'dataset/fc/customer_fc_10000_7.csv' 2
printf "Skenario 5 done\n"

python3 precompute.py 'dataset/fc/product_fc_20000_3.csv' 'dataset/fc/customer_fc_20000_3.csv' 2
printf "Skenario 6 done\n"

python3 precompute.py 'dataset/fc/product_fc_50000_3.csv' 'dataset/fc/customer_fc_50000_3.csv' 2
printf "Skenario 7 done\n"

python3 precompute.py 'dataset/fc/product_fc_100000_3.csv' 'dataset/fc/customer_fc_100000_3.csv' 2
printf "Skenario 8 done\n"

python3 precompute.py 'dataset/fc/product_fc_200000_3.csv' 'dataset/fc/customer_fc_200000_3.csv' 2
printf "Skenario 9 done\n"
