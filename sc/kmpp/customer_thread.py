"""
Semua kelas dan fungsi berkaitan dengan customer threading
"""

import threading

class CustomerThread(threading.Thread):
  def __init__(self, customer_id, customer_list=None, product_active=None, product_list=None):
    threading.Thread.__init__(self)
    self.thread_id = int(customer_id)
    self.name = "thread_c" + str(customer_id)
    self.customer_list = customer_list
    self.product_active = product_active
    self.product_list = product_list
    self.values = []
    self.stop_thread = False

  def kill_thread(self):
    self.stop_thread = True

  def run(self):
    # while self.stop_thread != True:
      print("\nStarting " + self.name)
      if self.product_active!=None:
        self.values = get_customer_values(self.thread_id, self.customer_list)
        init_dynamic_skyline(self.product_active, self.product_list, self.values, self.name)
      if self.stop_thread == True:
        print ("\nExiting " + self.name)

def get_customer_values(customer_id, customer_list):
  return customer_list[customer_id-1].values

def init_dynamic_skyline(product_active, product_list, values, thread_name):
  product_values = []
  customer_values = values
  count_product_active = product_active.copy()

  # ambil nilai produk
  while count_product_active:
    product = count_product_active.pop()
    product_values.append(product_list[product-1].values)

  # debug
  print('\nproduct values {}: {}'.format(thread_name, product_values))
  print('\ncustomer values {}: {}'.format(thread_name, customer_values))

def find_thread(threads, filter):
  counter = 0
  for thread in threads:
    if filter(thread):
      return counter
    counter += 1
    
def declare_threading_event():
  product_get_in = threading.Event()
  product_get_out = threading.Event()
  processing_product_in = threading.Event()
  processing_product_out = threading.Event()
  kill_thread = threading.Event()