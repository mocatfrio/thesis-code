import threading
from operator import itemgetter
from decimal import Decimal
from .logging import logger

class CustThread(threading.Thread):
  prod_data = None
  cust_data = None
  pandora_box = None

  def __init__(self, cust_id, timestamp, prod_active):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._event = threading.Event()
    self._work = threading.Event()
    self.id = cust_id
    self.name = "thread_c" + str(cust_id)
    self.timestamp = timestamp
    self.cust_values = CustThread.cust_data.get_values(cust_id)
    self.dsl_results = []
    self.dom_relation = {}
    self.last_updated = {}
    self.prod_active = prod_active
    self.product = None
    self.act = None
    self.last_event = None

  def update_prod_active(self, prod_active):
    self.prod_active = prod_active

  def notify(self, timestamp, product, act):
    self._event.set()
    self.timestamp = timestamp
    self.product = product
    self.act = act
  
  def is_done(self):
    return self._work.is_set() == False

  def get_last_event(self):
    logger.info('{} : last event {}'.format(self.name, self.last_event))
    return self.last_event

  def kill_thread(self, timestamp):
    self._event.set()
    self.timestamp = timestamp
    self.act = 2
    self._kill.set()

  def count_probability(self):
    try:
      return 1.0/len(self.dsl_results)
    except:
      return 0

  def process(self):
    if self.act == None:
      prod_values = get_values(CustThread.prod_data, self.prod_active)
    else:
      prod_values = get_values(CustThread.prod_data, self.product)      
    self.dsl_results, self.dom_relation = get_dynamic_skyline(self.dsl_results, self.cust_values, prod_values, self.dom_relation)      
    self.update_pandora_box()

  def update_pandora_box(self):
    CustThread.pandora_box.add_score(self.dsl_results, self.timestamp, self.count_probability(), self.last_updated)
    for dsl in self.dsl_results:
      self.last_updated[dsl[0]] = [self.timestamp, self.count_probability()]
      logger.info('Last update 2 pbox[{}] = {}'.format(dsl[0], self.last_updated.get(dsl[0])))

  def run(self):
    logger.info('{} starting..., ts: {}'.format(self.name, self.timestamp))
    self._work.set()
    if self.prod_active:
      logger.info("========================================================================")          
      logger.info('Initial dynamic skyline')
      self.process()
    self.last_event = 'init'
    self._work.clear()
    while not self._kill.is_set():
      if self._kill.is_set():
        break
      else:
        event = self._event.wait(3)
        if event:
          self._work.set()
          if self.act == 0: 
            logger.info("========================================================================")
            logger.info('Product {} in, ts: {}'.format(self.product, self.timestamp))
            self.process()
            self.last_event = 'p' + str(self.product[0]) + 'i'
          elif self.act == 1: 
            logger.info("========================================================================")            
            logger.info('Product {} out, ts: {}'.format(self.product, self.timestamp))
            index = check(self.product, self.dsl_results)
            if not index is None:
              if list(self.last_updated.get(self.product[0]))[0] != self.timestamp:
                CustThread.pandora_box.add_score(self.dsl_results, self.timestamp, self.count_probability(), self.last_updated)
              del self.dsl_results[index]
              del self.last_updated[self.product[0]]
              logger.info('DSL Results: {}'.format(self.dsl_results))
              self.prod_active = get_close_domination(self.dom_relation, self.product[0], self.prod_active)
              if self.prod_active:
                self.process()  
            self.last_event = 'p' + str(self.product[0]) + 'o'              
          elif self.act == 2:
            logger.info("========================================================================")    
            logger.info('{} exiting..., ts: {}'.format(self.name, self.timestamp))
            CustThread.pandora_box.add_score(self.dsl_results, self.timestamp, self.count_probability(), self.last_updated)
            self.last_event = 'killed'
          self._event.clear()
          self._work.clear()
    logger.info('{} killed'.format(self.name))

def check(val, array):
  for i in range(0, len(array)):
    if array[i][0] == val[0]:
      return i
  return None

def get_dynamic_skyline(current_dsl, cust_values, prod_values, dom_relation):
  prod_values = sorted(prod_values, key=itemgetter(1))
  logger.info('Customer values : {}'.format(cust_values))
  logger.info('Product values  : {}'.format(prod_values))
  # calc all diff
  for prod in prod_values:
    prod[1] = calc_diff(prod[1], cust_values)
    prod.append(0)
  if not current_dsl:
    dsl_results, dom_relation = compare(prod_values, prod_values, dom_relation)
  else:
    for dsl in current_dsl:
      dsl.append(0)
    dsl_results, dom_relation = compare(prod_values, current_dsl, dom_relation)
  logger.info('Close domination relationship: {}'.format(dom_relation))  
  return dsl_results, dom_relation    

def compare(val_a, val_b, dom):
  for i in range(0, len(val_a)):
    for j in range(0, len(val_b)):
      logger.info('[P-{}] diff : {} vs [P-{}] diff: {}'.format(val_a[i][0], val_a[i][1], val_b[j][0], val_b[j][1]))
      stat = check_dynamic_domination(val_a[i][1], val_b[j][1])
      if stat == 1:
        val_b[j][2] = 1
        dom = update_domination_relation(dom, val_a[i][0], val_b[j][0])
        logger.info('[P-{}] mendominasi [P-{}]'.format(val_a[i][0], val_b[j][0]))
      elif stat == 2:
        val_a[i][2] = 1
        dom = update_domination_relation(dom, val_b[j][0], val_a[i][0])
        logger.info('[P-{}] didominasi [P-{}]'.format(val_a[i][0], val_b[j][0]))
      else:
        logger.info('[P-{}] saling mendominasi dengan [P-{}]'.format(val_a[i][0], val_b[j][0]))
  dsl = get_dsl_result(val_a)  
  if val_b != val_a:
    dsl.extend(get_dsl_result(val_b))
  logger.info('DSL : {}'.format(dsl))
  return dsl, dom  

def get_dsl_result(val):
  dsl = []
  for i in range(0, len(val)):
    if val[i][2] == 0:
      new = []
      new.append(val[i][0])
      new.append(val[i][1])
      dsl.append(new)
  return dsl

def calc_diff(val_a, val_b):
  diff = []
  for col in range(0, len(val_a)):
    diff.append(abs(val_a[col] - val_b[col]))
  return diff

def update_domination_relation(storage, dominating, dominated):
  if dominating in storage:
    if dominated not in list(storage.get(dominating)):
      storage[dominating].append(dominated)
  else:
    storage[dominating] = [dominated]
  return storage

def check_dynamic_domination(val_a, val_b):
  equal = 0
  dominate = 0
  dominated = 0
  for col in range(0, len(val_a)):
    if val_a[col] <= val_b[col]:
      if val_a[col] < val_b[col]:
        dominate += 1
      equal += 1
    else:
      dominated += 1
  if equal == len(val_a):
    if dominate >= 1:
      if dominated < 1:
        return 1
      else:
        return 0
  else:
    if dominate < 1:
      return 2
    else: 
      return 0

def get_values(data, keys):
  prod_values = []
  for key in keys:
    new = []
    new.append(key)
    new.append(data.get_values(key))
    prod_values.append(new)
  return prod_values

def get_close_domination(dom_relation, prod, prod_active):
  dominated = []
  new = []
  if prod in dom_relation:
    dominated = list(dom_relation.get(prod))
    for dom in dominated:
      for value in dom_relation.values():
        if dom != value:
          new.append(dom)
          break
    logger.info('dominated1 = {}'.format(new))
    dominated = []    
    for t in new:
      if t not in prod_active:
        dominated.append(t)
    logger.info('dominated2 = {}'.format(dominated))      
  logger.info('product active now: {}'.format(prod_active))
  logger.info('Close domination: {} - {}'.format(prod, dominated))
  return dominated