import threading
import logging
from kmpp.dynamic_skyline import *

class CustomerThread(threading.Thread):
  mutex = threading.Lock()

  def __init__(self, customer_id=None, customer_list=None, pandora_box=None, event_id=None, product_active=None):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._product_in = threading.Event()
    self._product_out = threading.Event()
    self._init_dsl = False
    self.thread_id = customer_id
    self.name = "thread_c" + str(customer_id)
    self.customer_list = customer_list
    self.product_active = product_active
    self.pandora_box = pandora_box
    self.event_id = event_id

  def kill_thread(self):
    self._kill.set()

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
      if not self._init_dsl:
        if self.product_active is not None:
          logging.debug('Init dynamic skyline')
          dsl_result, probability = init_dynamic_skyline(self.thread_id, self.product_active, self.customer_list)
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
        