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
  product_list = input_csv('product', '../dataset/product.csv', ',', event_queue)
  customer_list = input_csv('customer', '../dataset/customer.csv', ',', event_queue)
  product_active = {}
  pandora_box = PandoraBox(len(product_list), event_queue.get_max_timestamp())

  logging.debug('Data Product')
  for product in product_list:
    product.display_data()
  logging.debug('Data Customer')
  for customer in customer_list:
    customer.display_data()

  # mengurutkan event
  event_queue.sort_queue()
  
  # inisialisasi thread master
  threads['master'] = CustomerThread()
  threads['master'].start()
  threads['master'].lock_mutex()

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
      logging.debug('[P-{} in] Processing product | waiting for lock'.format(queue[2]))
      threads['master'].lock_mutex()  
      logging.debug('[P-{} in] Processing product | unlocked'.format(queue[2]))
      product_active[queue[2]] = product_list[queue[2]-1].values
      logging.debug('[P-{} in] Masuk ke produk aktif: {}'.format(queue[2], product_active))

    elif queue[1] == 1 and queue[3] == 0:
      logging.debug('[P-{} out] Processing product | waiting for lock'.format(queue[2]))
      threads['master'].lock_mutex()  
      logging.debug('[P-{} in] Processing product | unlocked'.format(queue[2]))
      del product_active[queue[2]]
      logging.debug('[P-{} out] Hapus dari produk aktif: {}'.format(queue[2], product_active))

  for thread in threads:
    thread.join()

  logging.debug('Exiting the main program')  