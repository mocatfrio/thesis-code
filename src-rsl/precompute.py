import csv, sys
import numpy as np
from kmpp.customer_thread import CustThread
from kmpp.pandora_box import PandoraBox
from kmpp.event_queue import EventQueue
from kmpp.custom_logger import logger
from kmpp.reverse_skyline import ReverseSkyline

"""
Thread Handling
"""
def product_in(prod_id, threads, prod_active, timestamp, act, last_event):
  try:
    wait_thread_event(threads, last_event)
  finally:
    prod_active.append(prod_id)    
    logger.info('[P-{} in] Masuk ke produk aktif: {}'.format(prod_id, prod_active))  
    for thread in threads.values():
      thread.notify(timestamp, prod_id, act)

def product_out(prod_id, threads, prod_active, timestamp, act, last_event):
  try:
    wait_thread_event(threads, last_event)  
  finally:
    for thread in threads.values():
      thread.notify(timestamp, prod_id, act, prod_active.copy())
    prod_active.remove(prod_id)
    logger.info('[P-{} out] Hapus dari produk aktif: {}'.format(prod_id, prod_active))

def customer_in(cust_id, threads, prod_active, timestamp, last_event):
  try:
    wait_thread_event(threads, last_event)  
  finally:
    logger.info('[C-{} in] Make thread'.format(cust_id))
    threads[cust_id] = CustThread(int(cust_id), timestamp, prod_active.copy())
    threads[cust_id].start()

def customer_out(cust_id, threads, timestamp, last_event):
  while True:
    if threads[cust_id].get_last_event() == last_event or threads[cust_id].get_last_event() == 0 or threads[cust_id].get_last_event() == 1:
      break
  logger.info('[C-{} out] Kill thread'.format(cust_id))
  threads[cust_id].kill_thread(timestamp)

def insert_thread_data(data, pandora_box):
  CustThread.data = data
  CustThread.pandora_box = pandora_box 

def wait_thread_event(threads, last_event):
  while True:
    if all(thread.get_last_event() == last_event or thread.get_last_event() == 0 or thread.get_last_event() == 1 for thread in threads.values()):
      break

"""
Data Handling
"""
def input_csv(dataset, event_queue):
  data = {}
  for i in range(len(dataset)):
    logger.info('Input data {}'.format(dataset[i]))
    if i == 0:
      data['product'] = data_indexing(i, dataset[i])
    else:
      data['customer'] = data_indexing(i, dataset[i])
  return data

def data_indexing(data_id, data_file):
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
      data[id]['status'] = 0
      for i in range(4, col_cnt):
        data[id]['value'].append(int(row[csv_reader.fieldnames[i]]))
      for i in range(0, 2):
        event_queue.enqueue(data[id]['ts_in'] if i == 0 else data[id]['ts_out'], data_id, id, i)
  logger.info('Data ({}) succesfully inputed'.format(data_file))
  return data

def print_data(data):
  for key, values in data.items():
    logger.info('{}'.format(key))
    for k, v in values.items():
      logger.info('{} : {}'.format(k, v))

def get_max_value(data):
  all_val = []
  for val1 in data.values():
    for val2 in val1.values():
      all_val.append(val2['value'])
  return np.max(all_val, axis=0)

if __name__ == "__main__":
  data = {}
  event_queue = EventQueue()
  dataset = ['product.csv', 'customer.csv']
  data = input_csv(dataset, event_queue)
  print_data(data)
  max_val = get_max_value(data)

  event_queue.sort_queue()
  pandora_box = PandoraBox(len(data['product']) + 1, event_queue.get_max_timestamp() + 1)
  rsl_result = {}

  # komputasi RSL
  for k, v in data['product'].items():
    rsl = ReverseSkyline(k, data['product'], data['customer'], max_val)
    rsl.find_midpoint_skyline()
    rsl_result[k] = rsl.find_reverse_skyline()
  logger.info('{}'.format(rsl_result))

  # threads = {}
  # insert_thread_data(data, pandora_box)

  # Event
  while not event_queue.is_empty():
    event = event_queue.dequeue()
    if event[1] == 0:
      if event[3] == 0:
        """
        Product in
        """
        # product_in(event[2], threads, prod_active, event[0], event[3], last_event)
        # wait_thread_event(threads, last_event)
        data['product'][event[2]]['status'] = 1
        

      elif event[3] == 1:
        """
        Product out
        """
        data['product'][event[2]]['status'] = 0

        # product_out(event[2], threads, prod_active, event[0], event[3], last_event)
        # last_event = 'p' + str(event[2]) + 'o'
        # wait_thread_event(threads, last_event)
    elif event[1] == 1:
      if event[3] == 0:
        """
        Customer in
        """
        data['customer'][event[2]]['status'] = 1

        # customer_in(event[2], threads, prod_active, event[0], last_event)
      elif event[3] == 1:
        """
        Customer out
        """
        data['customer'][event[2]]['status'] = 0

        # customer_out(event[2], threads, event[0], last_event)

  # for thread in threads.values():
  #   thread.join()

  # pandora_box.print_box()
  # pandora_box.export_csv()

  # logger.info('Exiting the main program') 