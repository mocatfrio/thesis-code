import threading
import logging
import time
from kmpp.dynamic_skyline import *

class CustomerThread(threading.Thread):
  def __init__(self, customer_id=None, customer_list=None, pandora_box=None, timestamp=None, product_active=None):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._process_product = threading.Event()
    self._init_dsl = False
    self._status = False
    self.thread_id = customer_id
    self.name = "thread_c" + str(customer_id)
    self.customer_list = customer_list
    self.product_active = product_active
    self.pandora_box = pandora_box
    self.timestamp = timestamp
    self.action = 0

  def kill_thread(self):
    self._kill.set()

  def notify(self, timestamp, product, action):
    self._process_product.set()
    self.timestamp = timestamp
    self.product_active = product
    self.action = action

  def is_initialized(self):
    return self._init_dsl == True
  
  def is_done(self):
    return self._status == True

  def reset_status(self):
    self._status = False
    self._process_product.clear()

  def run(self):
    logging.debug('Starting')
    while not self._kill.is_set():
      if not self._init_dsl:
        if self.product_active is not None:
          logging.debug('Init dynamic skyline')
          dsl_result, probability = init_dynamic_skyline(self.thread_id, self.product_active, self.customer_list)
          self.pandora_box.add_score(dsl_result, self.timestamp, probability)
        self._init_dsl = True      
      else:
        if self._process_product.is_set():
          if self.action == 1:
            logging.debug("Process product in")
            if self.customer_list[self.thread_id-1].get_total_dsl() == 0:
              dsl_result = []
              for key in self.product_active.keys():
                dsl_result.append(key) 
              self.customer_list[self.thread_id-1].add_dsl(dsl_result)
              probability = self.customer_list[self.thread_id-1].count_probability()
              self.pandora_box.add_score(dsl_result, self.timestamp, probability)
            else:
              pass              
          else: 
            logging.debug("Process product out")
          self._status = True
      time.sleep(2)
      logging.debug('Killed? {}'.format(self._kill.is_set()))  
    logging.debug('Exiting')
