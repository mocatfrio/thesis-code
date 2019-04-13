from kmpp.data import *
from kmpp.event_queue import *
from kmpp.pandora_box import *
from kmpp.customer_thread import *
from logging_custom.logging import logger

def product_in(id, threads, prod_active, ts, act):
  while True:
    if all(thread.is_done() for key, thread in threads.items()):
      break
  prod_active.append(id)    
  logger.info('[P-{} in] Masuk ke produk aktif: {}'.format(id, prod_active))  
  for key, thread in threads.items():
    thread.notify(ts, [id], act)

def product_out(id, threads, prod_active, ts, act):
  while True:
    if all(thread.is_done() for key, thread in threads.items()):
      break
  for key, thread in threads.items():
    thread.notify(ts, [id], act, prod_active.copy())
  prod_active.remove(id)
  logger.info('[P-{} out] Hapus dari produk aktif: {}'.format(id, prod_active))

def customer_in(id, threads, prod_active, ts):
  logger.info('[C-{} in] Make thread'.format(id))
  if prod_active:
    threads[id] = CustThread(int(id), ts, prod_active.copy())
  else:
    threads[id] = CustThread(int(id), ts)
  threads[id].start()

def customer_out(id, threads):
  logger.info('[C-{} out] Kill thread'.format(id))
  # update pbox
  threads[id].kill_thread()

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
  CustThread.insert_data(prod_data, cust_data, pandora_box)
  # dequeue event
  while not event_queue.is_empty():
    event = event_queue.dequeue()
    if event[1] == 0:
      if event[3] == 0:
        product_in(event[2], threads, prod_active, event[0], event[3])
      elif event[3] == 1:
        product_out(event[2], threads, prod_active, event[0], event[3])
    elif event[1] == 1:
      if event[3] == 0:
        customer_in(event[2], threads, prod_active, event[0])
      elif event[3] == 1:
        customer_out(event[2], threads)
  # joining thread
  for key, thread in threads.items():
    thread.join()
  
  pandora_box.display()
  logger.info('Exiting the main program') 