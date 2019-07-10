import csv, sys, threading, os, time, cProfile, json
import numpy as np
from pandora_box import PandoraBox
from event_queue import EventQueue
from reverse_skyline import ReverseSkyline
from dynamic_skyline import DynamicSkyline
from logger import Logger
import multiprocessing
from multiprocessing import Pool

"""
Data Handling
"""
def input_csv(dataset, event_queue):
  data = {}
  for i in range(len(dataset)):
    if i == 0:
      data['product'] = {}
      data['product']['data'], data['product']['attr'] = data_indexing(i, dataset[i], event_queue)
    else:
      data['customer'] = {}
      data['customer']['data'], data['customer']['attr'] = data_indexing(i, dataset[i], event_queue)
  return data

def data_indexing(data_id, data_file, event_queue):
  data = {}
  with open(data_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
      attr = csv_reader.fieldnames
      col_cnt = len(attr)
      id = int(row[attr[0]])
      data[id] = {}
      data[id]['label'] = row[attr[1]]
      data[id]['ts_in'] = int(row[attr[2]])
      data[id]['ts_out'] = int(row[attr[3]])
      data[id]['value'] = []
      for i in range(4, col_cnt):
        data[id]['value'].append(int(row[attr[i]]))
      for i in range(0, 2):
        event_queue.enqueue(data[id]['ts_in'] if i == 0 else data[id]['ts_out'], data_id, id, i)
  return data, attr

def get_maxmin_value(product, customer):
  all_val = []
  for pid in product.values():
    all_val.append(pid['value'])
  for cid in customer.values():
    all_val.append(cid['value'])
  return np.max(all_val), np.min(all_val)

def get_metadata(event_queue, dataset, data):
  metadata = [
    event_queue.get_max_timestamp(), 
    event_queue.get_min_timestamp(),
    get_maxmin_value(data['product']['data'], data['customer']['data']),
    len(data['product']['attr']) - 4,
    len(data['product']['data']),
    len(data['customer']['data']),
    data['product']['attr'],
    data['customer']['attr'],
    dataset[0].split('/')[len(dataset[0].split('/'))-1],
    dataset[1].split('/')[len(dataset[1].split('/'))-1], 
  ]
  return metadata

"""
Event Handling
"""
def update_pbox(cust_id, ts, dsl, pandora_box, data):
  dsl.update(cust_id, ts)
  pandora_box.update(data['customer']['data'][cust_id]['dsl'])
  dsl.update_history(cust_id)

def compute_dsl(cust_id, ts, act, data_id, dsl):
  if act == 0:
    dsl.product_in(cust_id, ts, [data_id])
  else:
    dsl.product_out(cust_id, ts, data_id)
    dsl.update_history(cust_id)

def recheck(cust_id, ts, dsl, data):
  cand = set(data['product']['active']) - set(data['customer']['data'][cust_id]['dsl'].keys())
  if cand:
    cands = [c for c in cand]
    dsl.product_in(cust_id, ts, cands)

"""
Session Handling
"""
def make_session(data_info, algorithm, metadata):
  session_file = 'session'
  if not os.path.exists(session_file):
    os.mkdir(session_file)
  try:
    with open(session_file + '/session.json') as json_file:
      data = json.load(json_file)
      num = data['num']
  except:
    data = {}
    num = 0
  session_name = 'session_' + str(num+1) + '_' + data_info[1] + '_' + data_info[2] + '_' + data_info[3].split('.')[0] + '_' + algorithm
  my_data = {}
  my_data[session_name] = {
    'pbox_path': session_file + '/' + session_name + '/pandora_box.csv',
    'max_ts': metadata[0],
    'min_ts': metadata[1],
    'max_val': int(metadata[2][0]),
    'min_val': int(metadata[2][1]),
    'dim': metadata[3],
    'total_prod': metadata[4],
    'total_cust': metadata[5],
    'attr_prod': metadata[6],
    'attr_cust': metadata[7],
    'data_type': data_info[1],
    'product_data': metadata[8],
    'customer_data': metadata[9]
  }
  if 'session' in data:
    data['session'].update(my_data)
  else:
    data['session'] = my_data
  data['num'] = num + 1      
  with open(session_file + '/session.json', 'w') as json_file:
    json.dump(data, json_file)
  return session_name, session_file

"""
Precomputing
"""
def precompute_kmppti(dataset):
  algorithm = 'kmppti'
  logger = Logger(algorithm, 'precomputing')
  logger.set_time(0)
  logger.set_data_info(dataset[0].split('_'))
  print ('Precompute started')

  event_queue = EventQueue()
  data = {}
  data = input_csv(dataset, event_queue)
  event_queue.sort_queue()
  metadata = get_metadata(event_queue, dataset, data)

  data['product']['active'] = []
  data['customer']['active'] = []

  pandora_box = PandoraBox(metadata[4] + 1, metadata[0] + 1, data['product']['data'])
  rsl = ReverseSkyline(data['product'], data['customer'], metadata[3])
  dsl = DynamicSkyline(data['product'], data['customer'], metadata[3])

  while not event_queue.is_empty():
    event = event_queue.dequeue()
    print(event)
    if event[1] == 0:
      if event[3] == 0:
        data['product']['active'].append(event[2])
        rsl_result = rsl.compute(event[2])
        for cust_id in rsl_result:
          compute_dsl(cust_id, event[0], event[3], event[2], dsl)
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer']['data'][cust_id].keys():
            update_pbox(cust_id, event[0], dsl, pandora_box, data)
        
      elif event[3] == 1:
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer']['data'][cust_id].keys():
            update_pbox(cust_id, event[0], dsl, pandora_box, data)
        rsl_result = rsl.compute(event[2])
        for cust_id in rsl_result:
          compute_dsl(cust_id, event[0], event[3], event[2], dsl)
        data['product']['active'].remove(event[2])
        for cust_id in rsl_result:
          recheck(cust_id, event[0], dsl, data)
    
    elif event[1] == 1:
      if event[3] == 0:
        data['customer']['active'].append(event[2])
        dsl.customer_in(event[2], event[0])
        if 'dsl' in data['customer']['data'][event[2]].keys():
          pandora_box.update(data['customer']['data'][event[2]]['dsl'])
          dsl.update_history(event[2])

      elif event[3] == 1:
        dsl.update(event[2], event[0])
        if 'dsl' in data['customer']['data'][event[2]].keys():
          pandora_box.update(data['customer']['data'][event[2]]['dsl'])
          dsl.update_history(event[2])
        data['customer']['active'].remove(event[2])

  session_name, session_file = make_session(dataset[0].split('_'), algorithm, metadata)
  pandora_path = session_file + '/' + session_name
  os.mkdir(pandora_path)
  pandora_box.export_csv(pandora_path)

  logger.set_time(1)
  logger.set_runtime()
  logger.set_mem_usage()
  logger.export_log()

  return session_name

def precompute_kmppti_p(dataset):
  algorithm = 'kmppti-p'
  logger = Logger(algorithm, 'precomputing')
  logger.set_time(0)
  logger.set_data_info(dataset[0].split('_'))
  print ('Precompute started')

  event_queue = EventQueue()
  data = {}
  data = input_csv(dataset, event_queue)
  event_queue.sort_queue()
  metadata = get_metadata(event_queue, dataset, data)

  data['product']['active'] = []
  data['customer']['active'] = []

  pandora_box = PandoraBox(metadata[4] + 1, metadata[0] + 1, data['product']['data'])
  rsl = ReverseSkyline(data['product'], data['customer'], metadata[3])
  dsl = DynamicSkyline(data['product'], data['customer'], metadata[3])

  while not event_queue.is_empty():
    event = event_queue.dequeue()
    if event[1] == 0:
      if event[3] == 0:
        data['product']['active'].append(event[2])
        rsl_result = rsl.compute(event[2])
        all_cust = []
        for cust_id in rsl_result:
          all_cust.append([cust_id, event[0], event[3], event[2], dsl])
        if all_cust:
          pool = Pool(multiprocessing.cpu_count())
          pool.imap(compute_dsl, all_cust)
          pool.close()
          pool.join()
        all_cust = []
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer']['data'][cust_id].keys():
            all_cust.append([cust_id, event[0], dsl, pandora_box, data])
        if all_cust:
          pool = Pool(multiprocessing.cpu_count())
          pool.imap(update_pbox, all_cust)
          pool.close()
          pool.join()
        
      elif event[3] == 1:
        all_cust = []
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer']['data'][cust_id].keys():
            all_cust.append([cust_id, event[0], dsl, pandora_box, data])
        if all_cust:
          pool = Pool(multiprocessing.cpu_count())
          pool.imap(update_pbox, all_cust)
          pool.close()
          pool.join()
        rsl_result = rsl.compute(event[2])
        all_cust = []
        for cust_id in rsl_result:
          all_cust.append([cust_id, event[0], event[3], event[2], dsl])
        if all_cust:
          pool = Pool(multiprocessing.cpu_count())
          pool.imap(compute_dsl, all_cust)
          pool.close()
          pool.join()
        data['product']['active'].remove(event[2])
        all_cust = []
        for cust_id in rsl_result:
          all_cust.append([cust_id, event[0], dsl, data])
        if all_cust:
          pool = Pool(multiprocessing.cpu_count())
          pool.imap(recheck, all_cust)
          pool.close()
          pool.join()
    
    elif event[1] == 1:
      if event[3] == 0:
        data['customer']['active'].append(event[2])
        dsl.customer_in(event[2], event[0])
        if 'dsl' in data['customer']['data'][event[2]].keys():
          pandora_box.update(data['customer']['data'][event[2]]['dsl'])
          dsl.update_history(event[2])

      elif event[3] == 1:
        dsl.update(event[2], event[0])
        if 'dsl' in data['customer']['data'][event[2]].keys():
          pandora_box.update(data['customer']['data'][event[2]]['dsl'])
          dsl.update_history(event[2])
        data['customer']['active'].remove(event[2])

  session_name, session_file = make_session(dataset[0].split('_'), algorithm, metadata)
  pandora_path = session_file + '/' + session_name
  os.mkdir(pandora_path)
  pandora_box.export_csv(pandora_path)

  logger.set_time(1)
  logger.set_runtime()
  logger.set_mem_usage()
  logger.export_log()

  return session_name

def precompute_kmppti_norsl(dataset):
  algorithm = 'kmmpti-norsl'
  logger = Logger(algorithm, 'precomputing')
  logger.set_time(0)
  logger.set_data_info(dataset[0].split('_'))
  print ('Precompute started')

  event_queue = EventQueue()
  data = {}
  data = input_csv(dataset, event_queue)
  event_queue.sort_queue()
  metadata = get_metadata(event_queue, dataset, data)

  data['product']['active'] = []
  data['customer']['active'] = []

  pandora_box = PandoraBox(metadata[4] + 1, metadata[0] + 1, data['product']['data'])
  dsl = DynamicSkyline(data['product'], data['customer'], metadata[3])

  while not event_queue.is_empty():
    event = event_queue.dequeue()
    if event[1] == 0:
      if event[3] == 0:
        data['product']['active'].append(event[2])
        for cust_id in data['customer']['active']:
          compute_dsl(cust_id, event[0], event[3], event[2], dsl)
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer']['data'][cust_id].keys():
            update_pbox(cust_id, event[0], dsl, pandora_box, data)
        
      elif event[3] == 1:
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer']['data'][cust_id].keys():
            update_pbox(cust_id, event[0], dsl, pandora_box, data)
        for cust_id in data['customer']['active']:
          compute_dsl(cust_id, event[0], event[3], event[2], dsl)
        data['product']['active'].remove(event[2])
    
    elif event[1] == 1:
      if event[3] == 0:
        data['customer']['active'].append(event[2])
        dsl.customer_in(event[2], event[0])
        if 'dsl' in data['customer']['data'][event[2]].keys():
          pandora_box.update(data['customer']['data'][event[2]]['dsl'])
          dsl.update_history(event[2])

      elif event[3] == 1:
        dsl.update(event[2], event[0])
        if 'dsl' in data['customer']['data'][event[2]].keys():
          pandora_box.update(data['customer']['data'][event[2]]['dsl'])
          dsl.update_history(event[2])
        data['customer']['active'].remove(event[2])

  session_name, session_file = make_session(dataset[0].split('_'), algorithm, metadata)
  pandora_path = session_file + '/' + session_name
  os.mkdir(pandora_path)
  pandora_box.export_csv(pandora_path)

  logger.set_time(1)
  logger.set_runtime()
  logger.set_mem_usage()
  logger.export_log()

  return session_name

def precompute_kmppti_norslp(dataset):
  algorithm = 'kmmpti-norslp'
  logger = Logger(algorithm, 'precomputing')
  logger.set_time(0)
  logger.set_data_info(dataset[0].split('_'))
  print ('Precompute started')

  event_queue = EventQueue()
  data = {}
  data = input_csv(dataset, event_queue)
  event_queue.sort_queue()
  metadata = get_metadata(event_queue, dataset, data)

  data['product']['active'] = []
  data['customer']['active'] = []

  pandora_box = PandoraBox(metadata[4] + 1, metadata[0] + 1, data['product']['data'])
  dsl = DynamicSkyline(data['product'], data['customer'], metadata[3])

  while not event_queue.is_empty():
    event = event_queue.dequeue()
    if event[1] == 0:
      if event[3] == 0:
        data['product']['active'].append(event[2])
        threads = []
        for cust_id in data['customer']['active']:
          t = threading.Thread(target=compute_dsl, args=(cust_id, event[0], event[3], event[2], dsl))
          threads.append(t)
        for t in threads:
          t.start()
        for t in threads:
          t.join()
        threads = []
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer']['data'][cust_id].keys():
            t = threading.Thread(target=update_pbox, args=(cust_id, event[0], dsl, pandora_box, data))
            threads.append(t)
        for t in threads:
          t.start()
        for t in threads:
          t.join()
        
      elif event[3] == 1:
        threads = []
        for cust_id in data['customer']['active']:
          if 'dsl' in data['customer']['data'][cust_id].keys():
            t = threading.Thread(target=update_pbox, args=(cust_id, event[0], dsl, pandora_box, data))
            threads.append(t)
        for t in threads:
          t.start()
        for t in threads:
          t.join()
        threads = []
        for cust_id in data['customer']['active']:
          t = threading.Thread(target=compute_dsl, args=(cust_id, event[0], event[3], event[2], dsl))
          threads.append(t)
        for t in threads:
          t.start()
        for t in threads:
          t.join()
        data['product']['active'].remove(event[2])
    
    elif event[1] == 1:
      if event[3] == 0:
        data['customer']['active'].append(event[2])
        dsl.customer_in(event[2], event[0])
        if 'dsl' in data['customer']['data'][event[2]].keys():
          pandora_box.update(data['customer']['data'][event[2]]['dsl'])
          dsl.update_history(event[2])

      elif event[3] == 1:
        dsl.update(event[2], event[0])
        if 'dsl' in data['customer']['data'][event[2]].keys():
          pandora_box.update(data['customer']['data'][event[2]]['dsl'])
          dsl.update_history(event[2])
        data['customer']['active'].remove(event[2])

  session_name, session_file = make_session(dataset[0].split('_'), algorithm, metadata)
  pandora_path = session_file + '/' + session_name
  os.mkdir(pandora_path)
  pandora_box.export_csv(pandora_path)

  logger.set_time(1)
  logger.set_runtime()
  logger.set_mem_usage()
  logger.export_log()

  return session_name

if __name__ == "__main__":
  dataset = []
  dataset.append(sys.argv[1])
  dataset.append(sys.argv[2])
  algo = int(sys.argv[3])

  if algo == 1:
    precompute_kmppti(dataset)
  elif algo == 2:
    precompute_kmppti_norsl(dataset)
  elif algo == 3:
    precompute_kmppti_norslp(dataset)
  elif algo == 4:
    precompute_kmppti_p(dataset)