import csv
from app.src.kmpp.customer_thread import CustThread
from app.src.kmpp.pandora_box import PandoraBox
from app.src.kmpp.event_queue import EventQueue

def product_in(prod_id, threads, prod_active, timestamp, act, last_event):
  try:
    wait_thread_event(threads, last_event)
  finally:
    prod_active.append(prod_id)    
    for thread in threads.values():
      thread.notify(timestamp, prod_id, act)

def product_out(prod_id, threads, prod_active, timestamp, act, last_event):
  try:
    wait_thread_event(threads, last_event)  
  finally:
    for thread in threads.values():
      thread.notify(timestamp, prod_id, act, prod_active.copy())
    prod_active.remove(prod_id)

def customer_in(cust_id, threads, prod_active, timestamp, last_event):
  try:
    wait_thread_event(threads, last_event)  
  finally:
    threads[cust_id] = CustThread(int(cust_id), timestamp, prod_active.copy())
    threads[cust_id].start()

def customer_out(cust_id, threads, timestamp, last_event):
  while True:
    if threads[cust_id].get_last_event() == last_event or threads[cust_id].get_last_event() == 0 or threads[cust_id].get_last_event() == 1:
      break
  threads[cust_id].kill_thread(timestamp)

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

def insert_thread_data(data, pandora_box):
  CustThread.data = data
  CustThread.pandora_box = pandora_box 

def wait_thread_event(threads, last_event):
  while True:
    if all(thread.get_last_event() == last_event or thread.get_last_event() == 0 or thread.get_last_event() == 1 for thread in threads.values()):
      break

def kmpp_precompute(product_dataset, customer_product):
  event_queue = EventQueue()
  data = {}
  prod_active = []
  last_event = None
  data['product'] = input_csv('product', product_dataset, event_queue)
  data['customer'] = input_csv('customer', customer_product, event_queue)
  
  event_queue.sort_queue()
  pandora_box = PandoraBox(len(data['product']) + 1, event_queue.get_max_timestamp() + 1)
  threads = {}
  insert_thread_data(data, pandora_box)

  while not event_queue.is_empty():
    event = event_queue.dequeue()
    if event[1] == 0:
      if event[3] == 0:
        product_in(event[2], threads, prod_active, event[0], event[3], last_event)
        last_event = 'p' + str(event[2]) + 'i'
        wait_thread_event(threads, last_event)
      elif event[3] == 1:
        product_out(event[2], threads, prod_active, event[0], event[3], last_event)
        last_event = 'p' + str(event[2]) + 'o'
        wait_thread_event(threads, last_event)
    elif event[1] == 1:
      if event[3] == 0:
        customer_in(event[2], threads, prod_active, event[0], last_event)
      elif event[3] == 1:
        customer_out(event[2], threads, event[0], last_event)

  for thread in threads.values():
    thread.join()
    
  pandora_file = pandora_box.export_csv()

  return pandora_file