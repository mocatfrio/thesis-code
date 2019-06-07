import csv, sys, threading, os, time
import cProfile
# import logging
import numpy as np
from kmpp.pandora_box import PandoraBox
from kmpp.event_queue import EventQueue
from kmpp.reverse_skyline import ReverseSkyline
from kmpp.dynamic_skyline import DynamicSkyline

"""
Data Handling
"""
def input_csv(dataset, event_queue):
  data = {}
  for i in range(len(dataset)):
    # logging.info('Input data {}'.format(dataset[i]))
    if i == 0:
      data['product'] = data_indexing(i, dataset[i], event_queue)
    else:
      data['customer'] = data_indexing(i, dataset[i], event_queue)
  return data

def data_indexing(data_id, data_file, event_queue):
  data = {}
  with open(data_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
      col_cnt = len(csv_reader.fieldnames)
      id = int(row[csv_reader.fieldnames[0]])
      data[id] = {}
      data[id]['ts_in'] = int(row[csv_reader.fieldnames[2]])
      data[id]['ts_out'] = int(row[csv_reader.fieldnames[3]])
      data[id]['value'] = []
      for i in range(4, col_cnt):
        data[id]['value'].append(int(row[csv_reader.fieldnames[i]]))
      for i in range(0, 2):
        event_queue.enqueue(data[id]['ts_in'] if i == 0 else data[id]['ts_out'], data_id, id, i)
  # logging.info('Data ({}) succesfully inputed'.format(data_file))
  return data

# def print_data(data):
#   for key, values in data.items():
    # logging.info('{}'.format(key))
    # for k, v in values.items():
      # logging.info('\t {} : {}'.format(k, v))

def get_max_value(data):
  all_val = []
  for val1 in data.values():
    for val2 in val1.values():
      all_val.append(val2['value'])
  return np.max(all_val, axis=0)

def update_pbox(cust_id, ts, dsl, pandora_box, data):
  # logging.info('\t (1) c - {}'.format(cust_id))
  dsl.update(cust_id, ts)
  pandora_box.update(data['customer'][cust_id]['dsl'])
  dsl.update_history(cust_id)
  # logging.info('\t (1) c - {} SELESEI'.format(cust_id))  

def compute_dsl(cust_id, ts, act, data_id, dsl):
  if act == 0:
    dsl.product_in(cust_id, ts, [data_id])
  else:
    dsl.product_out(cust_id, ts, data_id)
    dsl.update_history(cust_id)

def recheck(cust_id, ts, dsl, data):
  # logging.info('\t (1) c - {}'.format(cust_id))  
  cand = set(data['product']['active']) - set(data['customer'][cust_id]['dsl'].keys())
  # logging.info('\t {} - {} = {}'.format(data['product']['active'], list(data['customer'][cust_id]['dsl'].keys()), cand))  
  if cand:
    cands = [c for c in cand]
    dsl.product_in(cust_id, ts, cands)

def main(dataset):
  data = {}
  event_queue = EventQueue()
  data = input_csv(dataset, event_queue)
  # print_data(data)
  event_queue.sort_queue()
  max_val = get_max_value(data)

  pandora_box = PandoraBox(len(data['product']) + 1, event_queue.get_max_timestamp() + 1)
  rsl = ReverseSkyline(data['product'], data['customer'], max_val)
  dsl = DynamicSkyline(data['product'], data['customer'], max_val, pandora_box)

  data['product']['active'] = []
  data['customer']['active'] = []

  # Event
  while not event_queue.is_empty():
    # logging.info('=================================================================')
    ts, role, data_id, act = event_queue.dequeue()
    
    if role == 0:
      if act == 0:
        # logging.info('[PRODUCT {} IN]'.format(data_id))
        data['product']['active'].append(data_id)
        # logging.info('(1) append to active products : {}'.format(data['product']['active']))  

        # logging.info('(2) compute RSL(p)')  
        rsl_result = rsl.compute(data_id)

        # logging.info('(3) for each RSL(p), compute DSL(c)')
        for cust_id in rsl_result:
          t = threading.Thread(target=compute_dsl, args=(cust_id, ts, act, data_id, dsl))
          t.start()
        for t in threading.enumerate():
          if t is not threading.current_thread():
            t.join()
        
        for cust_id in rsl_result:
          dsl.product_in(cust_id, ts, [data_id])

        # logging.info('(4) for c in CA, update pbox')
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer'][cust_id].keys():
            t = threading.Thread(target=update_pbox, args=(cust_id, ts, dsl, pandora_box, data))
            t.start()
        for t in threading.enumerate():
          if t is not threading.current_thread():
            t.join()
        
      elif act == 1:
        # logging.info('[PRODUCT {} OUT]'.format(data_id))
        # logging.info('(1) for c in CA, update PBox')
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer'][cust_id].keys():
            t = threading.Thread(target=update_pbox, args=(cust_id, ts, dsl, pandora_box, data))
            t.start()
        for t in threading.enumerate():
          if t is not threading.current_thread():
            t.join()
        
        # logging.info('(2) compute RSL(p)')  
        rsl_result = rsl.compute(data_id)

        # logging.info('(3) for each RSL(p), compute DSL(c)')  
        for cust_id in rsl_result:
          t = threading.Thread(target=compute_dsl, args=(cust_id, ts, act, data_id, dsl))
          t.start()
        for t in threading.enumerate():
          if t is not threading.current_thread():
            t.join()

        data['product']['active'].remove(data_id)
        # logging.info('(4) delete from active products : {}'.format(data['product']['active'])) 

        # logging.info('(5) recheck')
        for cust_id in rsl_result:
          t = threading.Thread(target=recheck, args=(cust_id, ts, dsl, data))
          t.start()
        for t in threading.enumerate():
          if t is not threading.current_thread():
            t.join()
    
    elif role == 1:
      if act == 0:
        # logging.info('[CUSTOMER {} IN]'.format(data_id))
        data['customer']['active'].append(data_id)
        # logging.info('(1) append to active customers : {}'.format(data['customer']['active']))

        # logging.info('(2) init DSL')
        dsl.customer_in(data_id, ts)
        
        # logging.info('(2) update PBox')
        if 'dsl' in data['customer'][data_id].keys():
          pandora_box.update(data['customer'][data_id]['dsl'])
          dsl.update_history(data_id)

      elif act == 1:
        # logging.info('[CUSTOMER {} OUT]'.format(data_id))
        dsl.update(data_id, ts)

        # logging.info('(1) update PBox')
        if 'dsl' in data['customer'][data_id].keys():
          pandora_box.update(data['customer'][data_id]['dsl'])
          dsl.update_history(data_id)

        data['customer']['active'].remove(data_id)
        # logging.info('(4) delete from active customers : {}'.format(data['customer']['active']))

      # logging.info('=================================================================')

  # pandora_box.print_box()
  pandora_box.export_csv()

  # logging.info('Exiting the main program') 

if __name__ == "__main__":
  if not os.path.exists('log'):
    os.mkdir('log')
  # logging.basicConfig(
  #     filename='log/app.log', 
  #     filemode='w', 
  #     # format='[%(levelname).1s] %(threadName)12s: %(message)s',
  #     format='[%(levelname).1s] %(message)s',
      # level=logging.INFO
  #   )
  # dataset = ['product.csv', 'customer.csv']
  dataset = ['product_i_500_2.csv', 'customer_i_500_2.csv']

  pr = cProfile.Profile()
  pr.enable()
  main(dataset)
  pr.disable()
  pr.print_stats()