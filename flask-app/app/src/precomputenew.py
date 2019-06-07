import csv, sys, threading, os, time
import cProfile
import numpy as np
from app.src.kmppnew.pandora_box import PandoraBox
from app.src.kmppnew.event_queue import EventQueue
from app.src.kmppnew.reverse_skyline import ReverseSkyline
from app.src.kmppnew.dynamic_skyline import DynamicSkyline
from app.src.kmppnew.logger import Logger

"""
Data Handling
"""
def input_csv(name, file, event_queue):
  data = {}
  with open(file, 'r') as csv_file:
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
        event_queue.enqueue(data[id]['ts_in'] if i == 0 else data[id]['ts_out'], 0 if name == 'product' else 1, id, i)
  return data
# def input_csv(dataset, event_queue):
#   data = {}
#   for i in range(len(dataset)):
#     if i == 0:
#       data['product'] = data_indexing(i, dataset[i], event_queue)
#     else:
#       data['customer'] = data_indexing(i, dataset[i], event_queue)
#   return data

# def data_indexing(data_id, data_file, event_queue):
#   data = {}
#   with open(data_file, 'r') as csv_file:
#     csv_reader = csv.DictReader(csv_file, delimiter=',')
#     for row in csv_reader:
#       col_cnt = len(csv_reader.fieldnames)
#       id = int(row[csv_reader.fieldnames[0]])
#       data[id] = {}
#       data[id]['ts_in'] = int(row[csv_reader.fieldnames[2]])
#       data[id]['ts_out'] = int(row[csv_reader.fieldnames[3]])
#       data[id]['value'] = []
#       for i in range(4, col_cnt):
#         data[id]['value'].append(int(row[csv_reader.fieldnames[i]]))
#       for i in range(0, 2):
#         event_queue.enqueue(data[id]['ts_in'] if i == 0 else data[id]['ts_out'], data_id, id, i)
#   return data

def get_max_value(data):
  all_val = []
  for val1 in data.values():
    for val2 in val1.values():
      all_val.append(val2['value'])
  return np.max(all_val, axis=0)

def update_pbox(cust_id, ts, dsl, pandora_box, data):
  dsl.update(cust_id, ts)
  pandora_box.update(data['customer'][cust_id]['dsl'])
  dsl.update_history(cust_id)

def compute_dsl(cust_id, ts, act, data_id, dsl):
  if act == 0:
    dsl.product_in(cust_id, ts, [data_id])
  else:
    dsl.product_out(cust_id, ts, data_id)
    dsl.update_history(cust_id)

def recheck(cust_id, ts, dsl, data):
  cand = set(data['product']['active']) - set(data['customer'][cust_id]['dsl'].keys())
  if cand:
    cands = [c for c in cand]
    dsl.product_in(cust_id, ts, cands)

def kmpp_precompute(product_dataset, customer_dataset):
  logger = Logger('kmppti-using-rsl', 'precomputing')
  logger.set_time(0)
  logger.set_data_info(product_dataset.split('_'))
  print ('Precompute started')

  event_queue = EventQueue()
  data = {}
  # data = input_csv(dataset, event_queue)
  data['product'] = input_csv('product', product_dataset, event_queue)
  data['customer'] = input_csv('customer', customer_dataset, event_queue)
  event_queue.sort_queue()
  max_val = get_max_value(data)

  pandora_box = PandoraBox(len(data['product']) + 1, event_queue.get_max_timestamp() + 1)
  rsl = ReverseSkyline(data['product'], data['customer'], max_val)
  dsl = DynamicSkyline(data['product'], data['customer'], max_val, pandora_box)

  data['product']['active'] = []
  data['customer']['active'] = []

  # Event
  while not event_queue.is_empty():
    ts, role, data_id, act = event_queue.dequeue()
    if role == 0:
      if act == 0:
        data['product']['active'].append(data_id)
        rsl_result = rsl.compute(data_id)
        threads = []
        for cust_id in rsl_result:
          t = threading.Thread(target=compute_dsl, args=(cust_id, ts, act, data_id, dsl))
          threads.append(t)
        for t in threads:
          t.start()
        for t in threads:
          t.join()
        for cust_id in rsl_result:
          dsl.product_in(cust_id, ts, [data_id])
        threads = []
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer'][cust_id].keys():
            t = threading.Thread(target=update_pbox, args=(cust_id, ts, dsl, pandora_box, data))
            threads.append(t)
        for t in threads:
          t.start()
        for t in threads:
          t.join()
        
      elif act == 1:
        threads = []
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer'][cust_id].keys():
            t = threading.Thread(target=update_pbox, args=(cust_id, ts, dsl, pandora_box, data))
            threads.append(t)
        for t in threads:
          t.start()
        for t in threads:
          t.join()
        rsl_result = rsl.compute(data_id)
        threads = []
        for cust_id in rsl_result:
          t = threading.Thread(target=compute_dsl, args=(cust_id, ts, act, data_id, dsl))
          threads.append(t)
        for t in threads:
          t.start()
        for t in threads:
          t.join()
        data['product']['active'].remove(data_id)
        threads = []
        for cust_id in rsl_result:
          t = threading.Thread(target=recheck, args=(cust_id, ts, dsl, data))
          threads.append(t)
        for t in threads:
          t.start()
        for t in threads:
          t.join()
    
    elif role == 1:
      if act == 0:
        data['customer']['active'].append(data_id)
        dsl.customer_in(data_id, ts)
        if 'dsl' in data['customer'][data_id].keys():
          pandora_box.update(data['customer'][data_id]['dsl'])
          dsl.update_history(data_id)

      elif act == 1:
        dsl.update(data_id, ts)
        if 'dsl' in data['customer'][data_id].keys():
          pandora_box.update(data['customer'][data_id]['dsl'])
          dsl.update_history(data_id)
        data['customer']['active'].remove(data_id)

  pandora_file = pandora_box.export_csv()

  logger.set_time(1)
  logger.set_runtime()
  logger.set_mem_usage()
  logger.export_log()

  return pandora_file

# if __name__ == "__main__":
#   if not os.path.exists('log'):
#     os.mkdir('log')
#   dataset = [os.getcwd()+'/app/upload/product_i_500_2.csv', os.getcwd()+'/app/upload/customer_i_500_2.csv']
#   print(dataset)

#   pr = cProfile.Profile()
#   pr.enable()
#   kmpp_precompute(dataset)
#   pr.disable()
#   pr.print_stats()