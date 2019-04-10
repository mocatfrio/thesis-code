from logging_custom.logging import logger
  
def get_dynamic_skyline(cust_values, prod_items):
  logger.info('Customer values : {}'.format(cust_values))
  logger.info('Product values : {}'.format(prod_items))

  dimension = len(sorted(prod_items.values())[0])
  rows = len(prod_items)
  prod_values = sorted(prod_items.values())
  prod_items = sorted(prod_items.keys(), key=prod_items.__getitem__)

  logger.info('Product values sorted : {}'.format(prod_values))
  logger.info('Product keys sorted : {}'.format(prod_items))
  
  for row in range(0, rows):
    current_diff = []
    if not all(x == None for x in prod_values[row]):
      for col in range(0, dimension):
        current_diff.append(abs(cust_values[col]-prod_values[row][col]))
      logger.info('[{}] Current diff : {}'.format(row, current_diff))

      for next_row in range(row+1, rows):
        if not all(x == None for x in prod_values[next_row]):
          next_diff = []
          for col in range(0, dimension):
            next_diff.append(abs(cust_values[col]-prod_values[next_row][col]))
          logger.info('[{}] Next diff : {}'.format(next_row, next_diff))

          stat = check_dynamic_domination(current_diff, next_diff, dimension)
          if stat == 1:
            prod_values[next_row] = [None for x in prod_values[next_row]]
            logger.info('[P-{}] mendominasi [P-{}]'.format(row, next_row))
          elif stat == 2:
            prod_values[row] = [None for x in prod_values[row]] 
            logger.info('[P-{}] didominasi [P-{}]'.format(row, next_row))
          else:
            logger.info('[P-{}] saling mendominasi dengan [P-{}]'.format(row, next_row))
        else:
          continue
    else:
      continue

  dsl_results = []
  for row in range(0, rows):
    if not all(x == None for x in prod_values[row]):
      dsl_results.append(prod_items[row])
  logger.info('Hasil Dynamic Skyline : {}'.format(dsl_results))
  return dsl_results

def update_dynamic_skyline(cust_values, dsl_results, new_prod):
  logger.info('Update dynamic skyline')  
  logger.info('Customer values : {}'.format(cust_values))
  logger.info('DSL values : {}'.format(dsl_results))
  logger.info('New product values : {}'.format(new_prod))

  new_dsl = []
  dimension = len(sorted(dsl_results.values())[0])
  rows = len(dsl_results)
  dsl_values = sorted(dsl_results.values())
  dsl_results = sorted(dsl_results.keys(), key=dsl_results.__getitem__)

  logger.info('DSL values sorted : {}'.format(dsl_values))
  logger.info('DSL keys sorted : {}'.format(dsl_results))

  current_diff = []
  for col in range(0, dimension):
    current_diff.append(abs(cust_values[col]-sorted(new_prod.values())[0][col]))
  logger.info('[P-new-{}] Current diff : {}'.format(sorted(new_prod.keys()), current_diff))
  
  for row in range(0, rows):
    next_diff = []
    for col in range(0, dimension):
      next_diff.append(abs(cust_values[col]-dsl_values[row][col]))
    logger.info('[{}] Next diff : {}'.format(row, next_diff))

    stat = check_dynamic_domination(current_diff, next_diff, dimension)
    if stat == 1:
      dsl_values[row] = [None for x in dsl_values[row]]
      if not sorted(new_prod.keys()) in dsl_results:
        dsl_results.append(sorted(new_prod.keys())) 
      logger.info('[P-new-{}] mendominasi [P-{}]'.format(sorted(new_prod)[0], row))
    elif stat == 2:
      # update CDG
      logger.info('[P-new-{}] didominasi [P-{}]'.format(sorted(new_prod)[0], row))
      new_dsl = dsl_results
      logger.info('Hasil UPDATE Dynamic Skyline : {}'.format(new_dsl))
      return new_dsl, 0
    else:
      logger.info('[P-new-{}] saling mendominasi dengan [P-{}]'.format(sorted(new_prod)[0], row))

  # hapus yg None, ambil key
  for row in range(0, rows):
    if not all(x == None for x in dsl_values[row]):
      new_dsl.append(dsl_results[row])
  new_dsl.append(sorted(new_prod)[0])
  logger.info('Hasil UPDATE Dynamic Skyline : {}'.format(new_dsl))
  return new_dsl, 1

def process_dsl(dsl_results, cust_id, cust_list, ts, pandora_box):
  cust_list[cust_id].add_dsl(dsl_results)
  probability = cust_list[cust_id].count_probability()
  pandora_box.add_score(dsl_results, ts, probability)

def get_dsl_values(cust_id, cust_list, p_list):
  product = {}
  for dsl in cust_list[cust_id].get_dsl():
      product[dsl] = p_list[dsl].get_values()
  logger.info('Mengambil hasil DSL: {}'.format(product))
  return product

def check_dynamic_domination(current_val, next_val, dim):
  equal = 0
  dominate = 0
  dominated = 0
  for col in range(0, dim):
    if current_val[col] <= next_val[col]:
      if current_val[col] < next_val[col]:
        dominate += 1
      equal += 1
    else:
      dominated += 1
  if equal == dim:
    if dominate >= 1:
      if dominated < 1:
        return 1
      else:
        return 0
  else:
    if dominate < 1:
      return 2
    else: 
      return 0