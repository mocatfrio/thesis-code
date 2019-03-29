import threading
import logging

from kmpp.data import *
from kmpp.event_queue import *
from kmpp.pandora_box import *
from kmpp.customer_thread import *

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename='kmpp.log', filemode='a', level=logging.DEBUG)

if __name__ == '__main__':
  event_queue = EventQueue()
  product_list = input_csv('product', '../dataset/product.csv', ',', event_queue)
  customer_list = input_csv('customer', '../dataset/customer.csv', ',', event_queue)
  product_active = []
  threads = []

  logging.debug('(main program)\tData Product')
  for product in product_list:
    product.display_data()
  logging.debug('(main program)\tData Customer')
  for customer in customer_list:
    customer.display_data()

  # mengurutkan event
  event_queue.sort_queue()
  
  # mengeluarkan event
  while not event_queue.is_empty():
    queue = event_queue.dequeue()
    logging.debug('(main program)\tDequeue event {}'.format(queue))
    
    if queue[1] == 0 and queue[3] == 1:
      logging.debug('(main program)\t[Customer {} in] Make thread'.format(queue[2]))
      if product_active:
        thread = CustomerThread(queue[2], customer_list, product_list, product_active)
      else:
        thread = CustomerThread(queue[2])
      thread.start()
      threads.append(thread)

    elif queue[1] == 0 and queue[3] == 0:
      logging.debug('(main program)\t[Customer {} out] Kill thread'.format(queue[2]))
      index = find_thread(threads, lambda x: x.thread_id == queue[2])
      threads[index].kill_thread()

    elif queue[1] == 1 and queue[3] == 1:
      logging.debug('(main program)\t[Product {} in] Processing product'.format(queue[2]))
      product_active.append(queue[2])
      logging.debug('(main program)\t[Product {}] Masuk ke produk aktif: {}'.format(queue[2], product_active))

    elif queue[1] == 1 and queue[3] == 0:
      logging.debug('(main program)\t[Product {}] Processing product'.format(queue[2]))
      product_active.remove(queue[2])
      logging.debug('(main program)\t[Product {}] Hapus dari produk aktif: {}'.format(queue[2], product_active))

  for thread in threads:
    thread.join()

  logging.debug('(main program)\tExiting the main program')  