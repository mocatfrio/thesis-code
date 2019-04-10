import threading
from kmpp.dynamic_skyline import *
from logging_custom.logging import logger

class CustThread(threading.Thread):
  cust_list = None
  prod_list = None
  pandora_box = None

  def __init__(self, cust_id, ts, prod_items=None):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._event = threading.Event()
    self._work = threading.Event()
    self.id = cust_id
    self.name = "thread_c" + str(cust_id)
    self.cust_values = CustThread.cust_list[cust_id].get_values()
    self.prod_items = prod_items
    self.ts = ts
    self.act = None

  def kill_thread(self):
    self._kill.set()

  def notify(self, ts, prod_items, act):
    self._event.set()
    self.ts = ts
    self.prod_items = prod_items
    self.act = act
  
  def is_done(self):
    return self._work.is_set() == False

  def run(self):
    logger.info('Starting')
    self._work.set()
    if self.prod_items is not None:
      logger.info('Init dynamic skyline')
      dsl_results = get_dynamic_skyline(self.cust_values, self.prod_items)
      process_dsl(dsl_results, self.id, CustThread.cust_list, self.ts, CustThread.pandora_box)
    self._work.clear()
    while not self._kill.is_set():
      event = self._event.wait(3)
      if event:
        self._work.set()
        if self.act == 1: 
          logger.info('Product in')
          if CustThread.cust_list[self.id].is_empty():
            dsl_results = sorted(self.prod_items)
            process_dsl(dsl_results, self.id, CustThread.cust_list, self.ts, CustThread.pandora_box)
          else:
            current_dsl = get_dsl_values(self.id, CustThread.cust_list, CustThread.prod_list)
            new_dsl, stat = update_dynamic_skyline(self.cust_values, current_dsl, self.prod_items)
            if stat == 0:
              CustThread.pandora_box.fill_score(new_dsl, self.ts)
            else:
              process_dsl(new_dsl, self.id, CustThread.cust_list, self.ts, CustThread.pandora_box)
        elif self.act == 0: 
          logger.info('Product out')
          #### coming soon
        self._event.clear()
        self._work.clear()
      logger.info('Killed? {}'.format(self._kill.is_set()))  
    logger.info('Exiting')