import logging
from operator import itemgetter

def init_dynamic_skyline(customer_id, product, customer_values, customer_list, timestamp, pandora_box):
  # get the value
  product_values = []
  for key, value in product.items():
    product_values.append(value)

  logging.debug('Product values : {}'.format(product_values))
  logging.debug('Customer values : {}'.format(customer_values))

  dsl_result = find_dynamic_skyline(product_values, customer_values, product)
  process_dsl_result(customer_id, customer_list, dsl_result, timestamp, pandora_box)
  
def process_dsl_result(customer_id, customer_list, dsl_result, timestamp, pandora_box):
  customer_list[customer_id-1].add_dsl(dsl_result)
  probability = customer_list[customer_id-1].count_probability()
  pandora_box.add_score(dsl_result, timestamp, probability)

def find_dynamic_skyline(product_values, customer_values, product):
  dimension = len(product_values[0])
  rows = len(product_values)
  product_values = sorted(product_values)
  logging.debug('Product values sorted : {}'.format(product_values))

  for row in range(0, rows):
    # menghitung selisih dgn baris saat ini
    now_diff = []
    if not all(x == None for x in product_values[row]):
      for col in range(0, dimension):
        now_diff.append(abs(customer_values[col]-product_values[row][col]))
      logging.debug('[{}] Now diff : {}'.format(row, now_diff))

      for next_row in range(row+1, rows):
        if not all(x == None for x in product_values[next_row]):
          # menghitung selisih dgn baris setelahnya
          next_diff = []
          for col in range(0, dimension):
            next_diff.append(abs(customer_values[col]-product_values[next_row][col]))
          logging.debug('[{}] Next diff : {}'.format(next_row, next_diff))

          # menentukan dominasi dinamis 
          equal = 0
          dominate = 0
          dominated = 0
          for col in range(0, dimension):
            if now_diff[col] <= next_diff[col]:
              if now_diff[col] < next_diff[col]:
                dominate += 1
              equal += 1
            else:
              dominated += 1
          if equal == dimension:
            if dominate >= 1:
              if dominated < 1:
                product_values[next_row] = [None for x in product_values[next_row]]
                logging.debug('[P-{}] mendominasi [P-{}]'.format(row, next_row))
              else:
                logging.debug('[P-{}] saling mendominasi [P-{}]'.format(row, next_row))
          else:
            if dominate < 1:
              product_values[row] = [None for x in product_values[row]] 
              logging.debug('[P-{}] didominasi [P-{}]'.format(row, next_row))
            else:
              logging.debug('[P-{}] saling mendominasi [P-{}]'.format(row, next_row))    
        else:
          continue
    else:
      continue

  # hapus yg None
  dsl_result = []
  for row in range(0, rows):
    if not all(x == None for x in product_values[row]):
      dsl_result.append(product_values[row])

  # cari product id
  for dsl in dsl_result:
    for key, value in product.items():
      if value == dsl:
        dsl_result[dsl_result.index(dsl)] = key
  logging.debug('Hasil Dynamic Skyline : {}'.format(dsl_result))
  
  return dsl_result

def take_value(customer_list, product_list):
  product_values = []

  return product_value
