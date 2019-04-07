import threading, logging
from kmpp.dynamic_skyline import *
from logging_custom.logging import logger

class CustomerThread(threading.Thread):
  customer_list = None
  product_list = None
  pandora_box = None

  def __init__(self, customer_id, timestamp, product=None):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._event = threading.Event()
    self._work = threading.Event()
    self.thread_id = customer_id
    self.name = "thread_c" + str(customer_id)
    self.customer_values = CustomerThread.customer_list[customer_id-1].get_values()
    self.product = product
    self.timestamp = timestamp
    self.action = 0

  def kill_thread(self):
    self._kill.set()

  def notify(self, timestamp, product, action):
    self._event.set()
    self.timestamp = timestamp
    self.product = product
    self.action = action
  
  def is_working(self):
    return self._work.is_set()

  def run(self):
    logger.debug('Starting')
    if self.product is not None:
      logger.debug('Init dynamic skyline')
      init_dynamic_skyline(self.thread_id, self.product, self.customer_values, CustomerThread.customer_list, self.timestamp, CustomerThread.pandora_box)
    while not self._kill.is_set():
      event = self._event.wait(3)
      if event:
        self._work.set()
        if self.action == 1: #product in
          logger.debug('Product in')
          if CustomerThread.customer_list[self.thread_id-1].is_empty():
            dsl_result = []
            for key in self.product.keys():
              dsl_result.append(key) 
            process_dsl_result(self.thread_id, CustomerThread.customer_list, dsl_result, self.timestamp, CustomerThread.pandora_box)
          else:
            product_values = take_value(self.thread_id, CustomerThread.customer_list, CustomerThread.product_list)

            pass 
        elif self.action == 1: 
          logger.debug('Product out')
        self._event.clear()
        self._work.clear()
      logger.debug('Killed? {}'.format(self._kill.is_set()))  
    logger.debug('Exiting')
