import threading
import logging
from kmpp.dynamic_skyline import *

class CustomerThread(threading.Thread):
  def __init__(self, customer_id, customer_list=None, product_list=None, product_active=None):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._product_in = threading.Event()
    self._product_out = threading.Event()
    self._init_dsl = False
    self.thread_id = int(customer_id)
    self.name = "thread_c" + str(customer_id)
    self.customer_list = customer_list
    self.product_list = product_list
    self.product_active = product_active

  def kill_thread(self):
    self._kill.set()

  def process_product_in(self):
    self._product_in.set()

  def process_product_out(self):
    self._product_out.set()

  def run(self):
    while not self._kill.is_set():
      logging.debug('({})\t\tStarting'.format(self.name))
      # jika belum diinisialisasi
      if not self._init_dsl:
        if self.product_active is not None:
          logging.debug('({})\t\tInit dynamic skyline'.format(self.name))
          init_dynamic_skyline(self.thread_id, self.product_active, self.product_list, self.customer_list, self.name)
        self._init_dsl = True
      killed = self._kill.wait(2)
      logging.debug('({})\t\tKilled? {}'.format(self.name, killed))
      if killed:
        logging.debug('({})\t\tExiting'.format(self.name))
        break
      else:
        logging.debug('({})\t\tProcess product? {}'.format(self.name, product_action))
        if product_action:
          logging.debug('({})\t\tLets process the product'.format(self.name))
        
def find_thread(threads, filter):
  counter = 0
  for thread in threads:
    if filter(thread):
      return counter
    counter += 1
