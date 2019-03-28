"""
Semua kelas dan fungsi berkaitan dengan customer threading
"""

import threading
import logging

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
      logging.debug('({})\t\tstarting'.format(self.name))
      if not self._init_dsl:
        if self.product_active is not None:
          logging.debug('({})\t\tinit dynamic skyline'.format(self.name))
          init_dynamic_skyline(self.thread_id, self.name, self.product_active, self.product_list, self.customer_list)
        self._init_dsl = True
      killed = self._kill.wait(2)
      logging.debug('({})\t\tkilled? {}'.format(self.name, killed))
      if killed:
        logging.debug('({})\t\texiting'.format(self.name))
        break
      else:
        logging.debug('({})\t\tprocess_product? {}'.format(self.name, product_action))
        if product_action:
          logging.debug('({})\t\tlets process the product'.format(self.name))
        
        
def init_dynamic_skyline(customer_id, thread_name, product_active, product_list, customer_list):
  product_values = []
  customer_values = customer_list[customer_id-1].values 
  count_product_active = product_active.copy()

  # ambil nilai produk
  while count_product_active:
    product = count_product_active.pop()
    product_values.append(product_list[product-1].values)

  logging.debug('({})\t\tproduct values : {}'.format(thread_name, product_values))
  logging.debug('({})\t\tcustomer values : {}'.format(thread_name, customer_values))

def find_thread(threads, filter):
  counter = 0
  for thread in threads:
    if filter(thread):
      return counter
    counter += 1
