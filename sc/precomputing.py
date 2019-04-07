import threading, logging
from kmpp.data import *
from kmpp.event_queue import *
from kmpp.pandora_box import *
from kmpp.customer_thread import *
from logging_custom.logging import logger

if __name__ == '__main__':
  event_queue = EventQueue()
  product_active = {}

  product_list = input_csv('product', '../dataset/product.csv', ',', event_queue)
  customer_list = input_csv('customer', '../dataset/customer.csv', ',', event_queue)
  event_queue.sort_queue()

  logger.debug('Queue')
  for row in event_queue.get_queue():
    logger.debug(row)
  
  pandora_box = PandoraBox(len(product_list)+2, event_queue.get_max_timestamp()+2)
  
  threads = {}
  CustomerThread.product_list = product_list
  CustomerThread.customer_list = customer_list
  CustomerThread.pandora_box = pandora_box

  logger.debug('Data Product')
  for product in product_list:
    logger.debug(product.get_data())
  logger.debug('Data Customer')
  for customer in customer_list:
    logger.debug(customer.get_data())

  # mengeluarkan event
  while not event_queue.is_empty():
    queue = event_queue.dequeue()
    logger.debug('Dequeue event {}'.format(queue))
    
    if queue[1] == 0 and queue[3] == 1:
      logger.debug('[C-{} in] Make thread'.format(queue[2]))
      if product_active:
        product = product_active.copy()
        threads[queue[2]] = CustomerThread(int(queue[2]), queue[0], product)
      else:
        threads[queue[2]] = CustomerThread(int(queue[2]), queue[0])
      threads[queue[2]].start()

    elif queue[1] == 0 and queue[3] == 0:
      logger.debug('[C-{} out] Kill thread'.format(queue[2]))
      threads[queue[2]].kill_thread()

    elif queue[1] == 1 and queue[3] == 1:
      while all(thread.is_working() for key, thread in threads.items()):
        logger.debug('Wait...')

      product = {}
      product[queue[2]] = product_list[queue[2]-1].values
      product_active.update(product)
      logger.debug('[P-{} in] Masuk ke produk aktif: {}'.format(queue[2], product_active))

      for key, thread in threads.items():
        thread.notify(queue[0], product, queue[3])

    elif queue[1] == 1 and queue[3] == 0:
      del product_active[queue[2]]
      logger.debug('[P-{} out] Hapus dari produk aktif: {}'.format(queue[2], product_active))

  for key, thread in threads.items():
    thread.join()

  logger.debug('Pandora Box')
  for row in pandora_box.get_pandora_box():
    logger.debug(row)

  logger.debug('Exiting the main program')  