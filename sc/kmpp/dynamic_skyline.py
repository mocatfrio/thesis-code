import logging
from operator import itemgetter
from logging_custom.logging import logger

def init_dynamic_skyline(customer_id, product, customer_values, customer_list, timestamp, pandora_box):
  logger.debug('Product values : {}'.format(product))
  logger.debug('Customer values : {}'.format(customer_values))

  dsl_result = find_dynamic_skyline(customer_values, product)
  process_dsl_result(customer_id, customer_list, dsl_result, timestamp, pandora_box)
  
def find_dynamic_skyline(customer_values, product):
  dimension = len(sorted(product.values())[0])
  rows = len(product)
  product_values = sorted(product.values())
  product = sorted(product, key=product.__getitem__)
  logger.debug('Product values sorted : {}'.format(product_values))
  logger.debug('Product keys sorted : {}'.format(product))

  for row in range(0, rows):
    # menghitung selisih dgn baris saat ini
    now_diff = []
    if not all(x == None for x in product_values[row]):
      for col in range(0, dimension):
        now_diff.append(abs(customer_values[col]-product_values[row][col]))
      logger.debug('[{}] Now diff : {}'.format(row, now_diff))

      for next_row in range(row+1, rows):
        if not all(x == None for x in product_values[next_row]):
          # menghitung selisih dgn baris setelahnya
          next_diff = []
          for col in range(0, dimension):
            next_diff.append(abs(customer_values[col]-product_values[next_row][col]))
          logger.debug('[{}] Next diff : {}'.format(next_row, next_diff))
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
                logger.debug('[P-{}] mendominasi [P-{}]'.format(row, next_row))
              else:
                logger.debug('[P-{}] saling mendominasi [P-{}]'.format(row, next_row))
          else:
            if dominate < 1:
              product_values[row] = [None for x in product_values[row]] 
              logger.debug('[P-{}] didominasi [P-{}]'.format(row, next_row))
            else:
              logger.debug('[P-{}] saling mendominasi [P-{}]'.format(row, next_row))    
        else:
          continue
    else:
      continue

  # hapus yg None, ambil key
  dsl_result = []
  for row in range(0, rows):
    if not all(x == None for x in product_values[row]):
      dsl_result.append(product[row])
  logger.debug('Hasil Dynamic Skyline : {}'.format(dsl_result))
  
  return dsl_result

def process_dsl_result(customer_id, customer_list, dsl_result, timestamp, pandora_box):
  customer_list[customer_id-1].add_dsl(dsl_result)
  probability = customer_list[customer_id-1].count_probability()
  pandora_box.add_score(dsl_result, timestamp, probability)

def take_value(customer_id, customer_list, product_list):
  product_values = []
  for product in customer_list[customer_id-1].get_dsl():
      pass

  return product_values
