#!/bin/bash

printf "================ TESTING INDEPENDENT START ================\n"

#python3 precompute.py 'dataset/ind/product_i_10000_3.csv' 'dataset/ind/customer_i_10000_3.csv' 1
#python3 precompute.py 'dataset/ind/product_i_10000_3.csv' 'dataset/ind/customer_i_10000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_10000_3.csv' 'dataset/ind/customer_i_10000_3.csv' 3
printf "Skenario 1 done\n"

#python3 precompute.py 'dataset/ind/product_i_10000_4.csv' 'dataset/ind/customer_i_10000_4.csv' 1
#python3 precompute.py 'dataset/ind/product_i_10000_4.csv' 'dataset/ind/customer_i_10000_4.csv' 2
python3 precompute.py 'dataset/ind/product_i_10000_4.csv' 'dataset/ind/customer_i_10000_4.csv' 3
printf "Skenario 2 done\n"

#python3 precompute.py 'dataset/ind/product_i_10000_5.csv' 'dataset/ind/customer_i_10000_5.csv' 1
#python3 precompute.py 'dataset/ind/product_i_10000_5.csv' 'dataset/ind/customer_i_10000_5.csv' 2
python3 precompute.py 'dataset/ind/product_i_10000_5.csv' 'dataset/ind/customer_i_10000_5.csv' 3
printf "Skenario 3 done\n"

#python3 precompute.py 'dataset/ind/product_i_10000_6.csv' 'dataset/ind/customer_i_10000_6.csv' 1
#python3 precompute.py 'dataset/ind/product_i_10000_6.csv' 'dataset/ind/customer_i_10000_6.csv' 2
python3 precompute.py 'dataset/ind/product_i_10000_6.csv' 'dataset/ind/customer_i_10000_6.csv' 3
printf "Skenario 4 done\n"

#python3 precompute.py 'dataset/ind/product_i_10000_7.csv' 'dataset/ind/customer_i_10000_7.csv' 1
#python3 precompute.py 'dataset/ind/product_i_10000_7.csv' 'dataset/ind/customer_i_10000_7.csv' 2
python3 precompute.py 'dataset/ind/product_i_10000_7.csv' 'dataset/ind/customer_i_10000_7.csv' 3
printf "Skenario 5 done\n"

#python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 1
#python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_20000_3.csv' 'dataset/ind/customer_i_20000_3.csv' 3
printf "Skenario 6 done\n"

#python3 precompute.py 'dataset/ind/product_i_50000_3.csv' 'dataset/ind/customer_i_50000_3.csv' 1
#python3 precompute.py 'dataset/ind/product_i_50000_3.csv' 'dataset/ind/customer_i_50000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_50000_3.csv' 'dataset/ind/customer_i_50000_3.csv' 3
printf "Skenario 7 done\n"

#python3 precompute.py 'dataset/ind/product_i_100000_3.csv' 'dataset/ind/customer_i_100000_3.csv' 1
#python3 precompute.py 'dataset/ind/product_i_100000_3.csv' 'dataset/ind/customer_i_100000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_100000_3.csv' 'dataset/ind/customer_i_100000_3.csv' 3
printf "Skenario 8 done\n"

#python3 precompute.py 'dataset/ind/product_i_200000_3.csv' 'dataset/ind/customer_i_200000_3.csv' 1
#python3 precompute.py 'dataset/ind/product_i_200000_3.csv' 'dataset/ind/customer_i_200000_3.csv' 2
python3 precompute.py 'dataset/ind/product_i_200000_3.csv' 'dataset/ind/customer_i_200000_3.csv' 3
printf "Skenario 9 done\n"

printf "================ TESTING ANTI-CORRELATED START ================\n"

#python3 precompute.py 'dataset/ant/product_ac_10000_3.csv' 'dataset/ant/customer_ac_10000_3.csv' 1
#python3 precompute.py 'dataset/ant/product_ac_10000_3.csv' 'dataset/ant/customer_ac_10000_3.csv' 2
python3 precompute.py 'dataset/ant/product_ac_10000_3.csv' 'dataset/ant/customer_ac_10000_3.csv' 3
printf "Skenario 1 done\n"

#python3 precompute.py 'dataset/ant/product_ac_10000_4.csv' 'dataset/ant/customer_ac_10000_4.csv' 1
#python3 precompute.py 'dataset/ant/product_ac_10000_4.csv' 'dataset/ant/customer_ac_10000_4.csv' 2
python3 precompute.py 'dataset/ant/product_ac_10000_4.csv' 'dataset/ant/customer_ac_10000_4.csv' 3
printf "Skenario 2 done\n"

#python3 precompute.py 'dataset/ant/product_ac_10000_5.csv' 'dataset/ant/customer_ac_10000_5.csv' 1
#python3 precompute.py 'dataset/ant/product_ac_10000_5.csv' 'dataset/ant/customer_ac_10000_5.csv' 2
python3 precompute.py 'dataset/ant/product_ac_10000_5.csv' 'dataset/ant/customer_ac_10000_5.csv' 3
printf "Skenario 3 done\n"

#python3 precompute.py 'dataset/ant/product_ac_10000_6.csv' 'dataset/ant/customer_ac_10000_6.csv' 1
#python3 precompute.py 'dataset/ant/product_ac_10000_6.csv' 'dataset/ant/customer_ac_10000_6.csv' 2
python3 precompute.py 'dataset/ant/product_ac_10000_6.csv' 'dataset/ant/customer_ac_10000_6.csv' 3
printf "Skenario 4 done\n"

#python3 precompute.py 'dataset/ant/product_ac_10000_7.csv' 'dataset/ant/customer_ac_10000_7.csv' 1
#python3 precompute.py 'dataset/ant/product_ac_10000_7.csv' 'dataset/ant/customer_ac_10000_7.csv' 2
python3 precompute.py 'dataset/ant/product_ac_10000_7.csv' 'dataset/ant/customer_ac_10000_7.csv' 3
printf "Skenario 5 done\n"

#python3 precompute.py 'dataset/ant/product_ac_20000_3.csv' 'dataset/ant/customer_ac_20000_3.csv' 1
#python3 precompute.py 'dataset/ant/product_ac_20000_3.csv' 'dataset/ant/customer_ac_20000_3.csv' 2
python3 precompute.py 'dataset/ant/product_ac_20000_3.csv' 'dataset/ant/customer_ac_20000_3.csv' 3
printf "Skenario 6 done\n"

#python3 precompute.py 'dataset/ant/product_ac_50000_3.csv' 'dataset/ant/customer_ac_50000_3.csv' 1
#python3 precompute.py 'dataset/ant/product_ac_50000_3.csv' 'dataset/ant/customer_ac_50000_3.csv' 2
python3 precompute.py 'dataset/ant/product_ac_50000_3.csv' 'dataset/ant/customer_ac_50000_3.csv' 3
printf "Skenario 7 done\n"

#python3 precompute.py 'dataset/ant/product_ac_100000_3.csv' 'dataset/ant/customer_ac_100000_3.csv' 1
#python3 precompute.py 'dataset/ant/product_ac_100000_3.csv' 'dataset/ant/customer_ac_100000_3.csv' 2
python3 precompute.py 'dataset/ant/product_ac_100000_3.csv' 'dataset/ant/customer_ac_100000_3.csv' 3
printf "Skenario 8 done\n"

#python3 precompute.py 'dataset/ant/product_ac_200000_3.csv' 'dataset/ant/customer_ac_200000_3.csv' 1
#python3 precompute.py 'dataset/ant/product_ac_200000_3.csv' 'dataset/ant/customer_ac_200000_3.csv' 2
python3 precompute.py 'dataset/ant/product_ac_200000_3.csv' 'dataset/ant/customer_ac_200000_3.csv' 3
printf "Skenario 9 done\n"

printf "================ TESTING FOREST-COVER START ================\n"

#python3 precompute.py 'dataset/fc/product_fc_10000_3.csv' 'dataset/fc/customer_fc_10000_3.csv' 1
#python3 precompute.py 'dataset/fc/product_fc_10000_3.csv' 'dataset/fc/customer_fc_10000_3.csv' 2
python3 precompute.py 'dataset/fc/product_fc_10000_3.csv' 'dataset/fc/customer_fc_10000_3.csv' 3
printf "Skenario 1 done\n"

#python3 precompute.py 'dataset/fc/product_fc_10000_4.csv' 'dataset/fc/customer_fc_10000_4.csv' 1
#python3 precompute.py 'dataset/fc/product_fc_10000_4.csv' 'dataset/fc/customer_fc_10000_4.csv' 2
python3 precompute.py 'dataset/fc/product_fc_10000_4.csv' 'dataset/fc/customer_fc_10000_4.csv' 3
printf "Skenario 2 done\n"

#python3 precompute.py 'dataset/fc/product_fc_10000_5.csv' 'dataset/fc/customer_fc_10000_5.csv' 1
#python3 precompute.py 'dataset/fc/product_fc_10000_5.csv' 'dataset/fc/customer_fc_10000_5.csv' 2
python3 precompute.py 'dataset/fc/product_fc_10000_5.csv' 'dataset/fc/customer_fc_10000_5.csv' 3
printf "Skenario 3 done\n"

#python3 precompute.py 'dataset/fc/product_fc_10000_6.csv' 'dataset/fc/customer_fc_10000_6.csv' 1
#python3 precompute.py 'dataset/fc/product_fc_10000_6.csv' 'dataset/fc/customer_fc_10000_6.csv' 2
python3 precompute.py 'dataset/fc/product_fc_10000_6.csv' 'dataset/fc/customer_fc_10000_6.csv' 3
printf "Skenario 4 done\n"

#python3 precompute.py 'dataset/fc/product_fc_10000_7.csv' 'dataset/fc/customer_fc_10000_7.csv' 1
#python3 precompute.py 'dataset/fc/product_fc_10000_7.csv' 'dataset/fc/customer_fc_10000_7.csv' 2
python3 precompute.py 'dataset/fc/product_fc_10000_7.csv' 'dataset/fc/customer_fc_10000_7.csv' 3
printf "Skenario 5 done\n"

#python3 precompute.py 'dataset/fc/product_fc_20000_3.csv' 'dataset/fc/customer_fc_20000_3.csv' 1
#python3 precompute.py 'dataset/fc/product_fc_20000_3.csv' 'dataset/fc/customer_fc_20000_3.csv' 2
python3 precompute.py 'dataset/fc/product_fc_20000_3.csv' 'dataset/fc/customer_fc_20000_3.csv' 3
printf "Skenario 6 done\n"

#python3 precompute.py 'dataset/fc/product_fc_50000_3.csv' 'dataset/fc/customer_fc_50000_3.csv' 1
#python3 precompute.py 'dataset/fc/product_fc_50000_3.csv' 'dataset/fc/customer_fc_50000_3.csv' 2
python3 precompute.py 'dataset/fc/product_fc_50000_3.csv' 'dataset/fc/customer_fc_50000_3.csv' 3
printf "Skenario 7 done\n"

#python3 precompute.py 'dataset/fc/product_fc_100000_3.csv' 'dataset/fc/customer_fc_100000_3.csv' 1
#python3 precompute.py 'dataset/fc/product_fc_100000_3.csv' 'dataset/fc/customer_fc_100000_3.csv' 2
python3 precompute.py 'dataset/fc/product_fc_100000_3.csv' 'dataset/fc/customer_fc_100000_3.csv' 3
printf "Skenario 8 done\n"

#python3 precompute.py 'dataset/fc/product_fc_200000_3.csv' 'dataset/fc/customer_fc_200000_3.csv' 1
#python3 precompute.py 'dataset/fc/product_fc_200000_3.csv' 'dataset/fc/customer_fc_200000_3.csv' 2
python3 precompute.py 'dataset/fc/product_fc_200000_3.csv' 'dataset/fc/customer_fc_200000_3.csv' 3
printf "Skenario 9 done\n"
