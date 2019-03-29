import logging
from operator import itemgetter

def init_dynamic_skyline(customer_id, product_active, product_list, customer_list, thread_name):
  product_values = []
  customer_values = customer_list[customer_id-1].values 
  count_product_active = product_active.copy()

  # ambil nilai produk
  while count_product_active:
    product = count_product_active.pop()
    product_values.append(product_list[product-1].values)

  logging.debug('({})\t\tProduct values : {}'.format(thread_name, product_values))
  logging.debug('({})\t\tCustomer values : {}'.format(thread_name, customer_values))

  find_dynamic_skyline(product_values, customer_values, thread_name)

def find_dynamic_skyline(product_values, customer_values, thread_name):
  dimensions = len(product_values[0])
  rows = len(product_values)
  product_values = sorted(product_values, key=itemgetter(0, dimensions-1)) #dimensi belum dinamis
  logging.debug('({})\t\tProduct values sorted : {}'.format(thread_name, product_values))

  for row in range(0, rows):
    # menghitung selisih
    now_diff = []
    for col in range(0, dimensions):
      now_diff.append(abs(customer_values[col]-product_values[row][col]))
    logging.debug('({})\t\t[{}] Now diff : {}'.format(thread_name, row, now_diff))

    for next_row in range(row+1, rows):
      # menghitung selisih setelahnya, diiterasi
      next_diff = []
      for col in range(0, dimensions):
        next_diff.append(abs(customer_values[col]-product_values[next_row][col]))
      logging.debug('({})\t\t[{}] Next diff : {}'.format(thread_name, next_row, next_diff))

      # menentukan dynamic skyline
      less_than_eq = 0
      less_than = 0
      for col in range(0, dimensions):
        if now_diff[col] <= next_diff[col]:
          if now_diff[col] < next_diff[col]:
            less_than += 1
          less_than_eq += 1
      if less_than_eq == dimensions:
        if less_than >= 1:
          if less_than == dimensions:
            logging.debug('({})\t\t[p{}] mendominasi p{}'.format(thread_name, row, next_row))
          else:
            logging.debug('({})\t\t[p{}] saling mendominasi p{}'.format(thread_name, row, next_row))
      else:
        if less_than == 0:
          logging.debug('({})\t\t[p{}] didominasi p{}'.format(thread_name, row, next_row))
        else:
          logging.debug('({})\t\t[p{}] saling mendominasi p{}'.format(thread_name, row, next_row))

  logging.debug('({})\t\tHasil Dynamic Skyline : {}'.format(thread_name, product_values))
