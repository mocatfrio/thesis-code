from kmpp.data import *
from kmpp.event_queue import *
from kmpp.pandora_box import *
from kmpp.customer_thread import *
from logging_custom.logging import logger

if __name__ == '__main__':
  event_queue = EventQueue()
  prod_active = {}

  prod_list = input_csv('product', '../dataset/product.csv', ',', event_queue)
  cust_list = input_csv('customer', '../dataset/customer.csv', ',', event_queue)
  event_queue.sort_queue()

  logger.info('Queue')
  for row in event_queue.get_queue():
    logger.info(row)
  
  pandora_box = PandoraBox(len(prod_list) + 2, event_queue.get_max_timestamp() + 2)
  
  threads = {}
  CustThread.prod_list = prod_list
  CustThread.cust_list = cust_list
  CustThread.pandora_box = pandora_box

  logger.info('Data Product')
  for id in range(1, len(prod_list)):
    logger.info(prod_list[id].get_data())
  logger.info('Data Customer')
  for id in range(1, len(cust_list)): 
    logger.info(cust_list[id].get_data())

  # mengeluarkan event
  while not event_queue.is_empty():
    event = event_queue.dequeue()
    logger.info('Dequeue event {}'.format(event))
    
    if event[1] == 0:
      if event[3] == 1:
        logger.info('[C-{} in] Make thread'.format(event[2]))
        if prod_active:
          prod_items = prod_active.copy()
          threads[event[2]] = CustThread(int(event[2]), event[0], prod_items)
        else:
          threads[event[2]] = CustThread(int(event[2]), event[0])
        threads[event[2]].start()
      elif event[3] == 0:
        logger.info('[C-{} out] Kill thread'.format(event[2]))
        threads[event[2]].kill_thread()
    elif event[1] == 1:
      if event[3] == 1:
        while not all(thread.is_done() for key, thread in threads.items()):
          logger.info('Wait...')
        prod_items = {}
        prod_items[event[2]] = prod_list[event[2]].get_values()
        prod_active.update(prod_items)
        logger.info('[P-{} in] Masuk ke produk aktif: {}'.format(event[2], prod_active))
        for key, thread in threads.items():
          thread.notify(event[0], prod_items, event[3])
      elif event[3] == 0:
        del prod_active[event[2]]
        logger.info('[P-{} out] Hapus dari produk aktif: {}'.format(event[2], prod_active))

  for key, thread in threads.items():
    thread.join()

  logger.info('Pandora Box')
  for row in pandora_box.get_pandora_box():
    logger.info(row)

  logger.info('Exiting the main program') 