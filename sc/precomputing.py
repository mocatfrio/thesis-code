import threading
import logging
from kmpp.data import *
from kmpp.event_queue import *
from kmpp.pandora_box import *
from kmpp.customer_thread import *

logging.basicConfig(filename='../kmpp.log', 
                    filemode='w', level=logging.DEBUG, 
                    format='[%(levelname)s] (%(threadName)-9s) %(message)s')

if __name__ == '__main__':
  threads = {}
  event_queue = EventQueue()
  product_active = {}

  product_list = input_csv('product', '../dataset/product.csv', ',', event_queue)
  customer_list = input_csv('customer', '../dataset/customer.csv', ',', event_queue)
  event_queue.sort_queue()

  logging.debug('===============================================')
  logging.debug('Queue')
  for row in event_queue.get_queue():
    logging.debug(row)
  
  pandora_box = PandoraBox(len(product_list)+2, event_queue.get_max_timestamp()+2)

  logging.debug('===============================================')
  logging.debug('Data Product')
  for product in product_list:
    logging.debug(product.get_data())
  logging.debug('===============================================')
  logging.debug('Data Customer')
  for customer in customer_list:
    logging.debug(customer.get_data())

  # mengeluarkan event
  while not event_queue.is_empty():
    queue = event_queue.dequeue()
    logging.debug('Dequeue event {}'.format(queue))
    
    if queue[1] == 0 and queue[3] == 1:
      logging.debug('[C-{} in] Make thread'.format(queue[2]))
      if product_active:
        threads[queue[2]] = CustomerThread(int(queue[2]), customer_list, pandora_box, queue[0], product_active)
      else:
        threads[queue[2]] = CustomerThread(int(queue[2]), customer_list, pandora_box, queue[0])
      threads[queue[2]].start()

    elif queue[1] == 0 and queue[3] == 0:
      logging.debug('[C-{} out] Kill thread'.format(queue[2]))
      threads[queue[2]].kill_thread()

    elif queue[1] == 1 and queue[3] == 1:
      while not all(thread.is_initialized() for key, thread in threads.items()):
        logging.debug('Waiting all threads are initialized')

      product = {}
      product[queue[2]] = product_list[queue[2]-1].values
      product_active.update(product)
      logging.debug('[P-{} in] Masuk ke produk aktif: {}'.format(queue[2], product_active))

      for key, thread in threads.items():
        thread.notify(queue[0], product, queue[3])

      while not all(thread.is_done() for key, thread in threads.items()):
        logging.debug('Waiting all threads are done')
      
      for key, thread in threads.items():
        thread.reset_status()

    elif queue[1] == 1 and queue[3] == 0:
      while not all(thread.is_initialized() for key, thread in threads.items()):
        logging.debug('Waiting thread init')

      del product_active[queue[2]]
      logging.debug('[P-{} out] Hapus dari produk aktif: {}'.format(queue[2], product_active))

      # process

  for key, thread in threads.items():
    thread.join()

  logging.debug('===============================================')
  logging.debug('Pandora Box')
  for row in pandora_box.get_pandora_box():
    logging.debug(row)

  logging.debug('Exiting the main program')  