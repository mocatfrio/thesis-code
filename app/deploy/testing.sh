# echo "TESTING INDEPENDENT"

# python3 precompute.py dataset/ind/product_i_10000_3.csv dataset/ind/customer_i_10000_3.csv 2
# python3 precompute.py dataset/ind/product_i_10000_3.csv dataset/ind/customer_i_10000_3.csv 3
# python3 precompute.py dataset/ind/product_i_10000_3.csv dataset/ind/customer_i_10000_3.csv 1

# echo "2000 7 done"

echo "TESTING ANTI-CORRELATED"

python3 precompute.py dataset/ant/product_ac_10000_3.csv dataset/ant/customer_ac_10000_3.csv 2
python3 precompute.py dataset/ant/product_ac_10000_3.csv dataset/ant/customer_ac_10000_3.csv 3
python3 precompute.py dataset/ant/product_ac_10000_3.csv dataset/ant/customer_ac_10000_3.csv 1

echo "10000 3 done"

# python3 precompute.py dataset/ant/product_ac_2000_7.csv dataset/ant/customer_ac_2000_7.csv 1
# python3 precompute.py dataset/ant/product_ac_2000_7.csv dataset/ant/customer_ac_2000_7.csv 2
# python3 precompute.py dataset/ant/product_ac_2000_7.csv dataset/ant/customer_ac_2000_7.csv 3

# echo "2000 7 done"

# echo "TESTING FORESTCOVER"

# python3 precompute.py dataset/fc/product_fc_2000_4.csv dataset/fc/customer_fc_2000_4.csv 1
# python3 precompute.py dataset/fc/product_fc_2000_4.csv dataset/fc/customer_fc_2000_4.csv 2
# python3 precompute.py dataset/fc/product_fc_2000_4.csv dataset/fc/customer_fc_2000_4.csv 3

# echo "2000 4 done"

# python3 precompute.py dataset/fc/product_fc_2000_5.csv dataset/fc/customer_fc_2000_5.csv 1
# python3 precompute.py dataset/fc/product_fc_2000_5.csv dataset/fc/customer_fc_2000_5.csv 2
# python3 precompute.py dataset/fc/product_fc_2000_5.csv dataset/fc/customer_fc_2000_5.csv 3

# echo "2000 5 done"

# python3 precompute.py dataset/fc/product_fc_2000_7.csv dataset/fc/customer_fc_2000_7.csv 3
# echo "2000 7 3 done"

# # python3 precompute.py dataset/fc/product_fc_2000_6.csv dataset/fc/customer_fc_2000_6.csv 2
# # python3 precompute.py dataset/fc/product_fc_2000_6.csv dataset/fc/customer_fc_2000_6.csv 3
# python3 precompute.py dataset/fc/product_fc_2000_6.csv dataset/fc/customer_fc_2000_6.csv 1

# echo "2000 6 1 done"

# python3 precompute.py dataset/fc/product_fc_2000_7.csv dataset/fc/customer_fc_2000_7.csv 2
# python3 precompute.py dataset/fc/product_fc_2000_7.csv dataset/fc/customer_fc_2000_7.csv 1

# echo "2000 7 1 done"