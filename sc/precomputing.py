from kmpp.data import Data, input_csv
from kmpp.event_queue import EventQueue
from kmpp.pandora_box import *
from kmpp.customer_thread import CustThread
from kmpp.logging import logger

def product_in(id, threads, prod_active, timestamp, act, last_event):
  wait_thread_event(threads, last_event)
  prod_active.append(id)    
  logger.info('[P-{} in] Masuk ke produk aktif: {}'.format(id, prod_active))  
  for thread in threads.values():
    thread.notify(timestamp, [id], act)
  wait_thread(threads)  

def product_out(id, threads, prod_active, timestamp, act, last_event):
  wait_thread_event(threads, last_event)  
  for thread in threads.values():
    thread.notify(timestamp, [id], act)
    thread.update_prod_active(prod_active.copy())
  prod_active.remove(id)
  logger.info('[P-{} out] Hapus dari produk aktif: {}'.format(id, prod_active))

def customer_in(id, threads, prod_active, timestamp, last_event):
  try:
    wait_thread_event(threads, last_event)  
  finally:
    logger.info('[C-{} in] Make thread'.format(id))
    threads[id] = CustThread(int(id), timestamp, prod_active.copy())
    threads[id].start()

def customer_out(id, threads, timestamp, last_event):
  while True:
    if threads[id].get_last_event() == last_event:
      break
  logger.info('[C-{} out] Kill thread'.format(id))
  threads[id].kill_thread(timestamp)

def insert_thread_data(prod_data, cust_data, pandora_box):
  CustThread.prod_data = prod_data
  CustThread.cust_data = cust_data
  CustThread.pandora_box = pandora_box 

def wait_thread(threads):
  while True:
    if all(thread.is_done() for thread in threads.values()):
      break

def wait_thread_event(threads, last_event):
  while True:
    logger.info('{}'.format(last_event))
    if all(thread.get_last_event() == last_event or thread.get_last_event() == 'init' or thread.get_last_event() == 'killed' for thread in threads.values()):
      break

if __name__ == '__main__':
  event_queue = EventQueue()
  prod_data, cust_data = Data(), Data()
  prod_active = []

  # input data
  dataset = ['../dataset/product.csv', '../dataset/customer.csv']
  input_csv('p', dataset[0], event_queue, prod_data)
  input_csv('c', dataset[1], event_queue, cust_data)

  # sorting queue
  event_queue.sort_queue()

  # instantiate pandora box
  pandora_box = PandoraBox(prod_data.get_total_data() + 1, event_queue.get_max_timestamp() + 1)

  # instantiate thread
  threads = {}
  insert_thread_data(prod_data, cust_data, pandora_box)

  last_event = None

  # dequeue event
  while not event_queue.is_empty():
    event = event_queue.dequeue()
    if event[1] == 0:
      if event[3] == 0:
        product_in(event[2], threads, prod_active, event[0], event[3], last_event)
        last_event = 'p' + str(event[2]) + 'i'
      elif event[3] == 1:
        product_out(event[2], threads, prod_active, event[0], event[3], last_event)
        last_event = 'p' + str(event[2]) + 'o'
    elif event[1] == 1:
      if event[3] == 0:
        customer_in(event[2], threads, prod_active, event[0], last_event)
      elif event[3] == 1:
        customer_out(event[2], threads, event[0], last_event)

  # joining thread
  for thread in threads.values():
    thread.join()
  
  pandora_box.display()

  logger.info('Exiting the main program') 