import threading
import logging
<<<<<<< HEAD
import time
from kmpp.dynamic_skyline import *

class CustomerThread(threading.Thread):
  def __init__(self, customer_id=None, customer_list=None, pandora_box=None, timestamp=None, product_active=None):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._process_product = threading.Event()
    self._init_dsl = False
    self._status = False
=======
from kmpp.dynamic_skyline import *

class CustomerThread(threading.Thread):
  mutex = threading.Lock()

  def __init__(self, customer_id=None, customer_list=None, pandora_box=None, event_id=None, product_active=None):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._product_in = threading.Event()
    self._product_out = threading.Event()
    self._init_dsl = False
>>>>>>> 21b379e784cc4ec6a53a19da9bfdb905928da0a7
    self.thread_id = customer_id
    self.name = "thread_c" + str(customer_id)
    self.customer_list = customer_list
    self.product_active = product_active
    self.pandora_box = pandora_box
<<<<<<< HEAD
    self.timestamp = timestamp
    self.action = 0
=======
    self.event_id = event_id
>>>>>>> 21b379e784cc4ec6a53a19da9bfdb905928da0a7

  def kill_thread(self):
    self._kill.set()

<<<<<<< HEAD
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
=======
  def process_product_in(self):
    self._product_in.set()

  def process_product_out(self):
    self._product_out.set()
  
  def lock_mutex(self):
    CustomerThread.mutex.acquire()

  def unlock_mutex(self):
    CustomerThread.mutex.release()

  def run(self):
    while not self._kill.is_set():
      logging.debug('Starting')
      # jika belum diinisialisasi
>>>>>>> 21b379e784cc4ec6a53a19da9bfdb905928da0a7
      if not self._init_dsl:
        if self.product_active is not None:
          logging.debug('Init dynamic skyline')
          dsl_result, probability = init_dynamic_skyline(self.thread_id, self.product_active, self.customer_list)
<<<<<<< HEAD
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
=======
          self.unlock_mutex()
          self.pandora_box.add_score(dsl_result, self.event_id, probability)
        else:
          self.unlock_mutex()
        self._init_dsl = True
      killed = self._kill.wait(2)
      logging.debug('Killed? {}'.format(killed))
      if killed:
        logging.debug('Exiting')
        break
      else:
        logging.debug('Lets process the product')
        
>>>>>>> 21b379e784cc4ec6a53a19da9bfdb905928da0a7
