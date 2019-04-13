import threading
from operator import itemgetter
from logging_custom.logging import logger

class CustThread(threading.Thread):
  prod_data = None
  cust_data = None
  pandora_box = None

  def __init__(self, cust_id, ts, prod_active=None):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._event = threading.Event()
    self._work = threading.Event()
    self.id = cust_id
    self.name = "thread_c" + str(cust_id)
    self.cust_values = CustThread.cust_data.get_values(cust_id)
    self.dsl_results = {}
    self.dom_relation = {}
    self.prod_active = prod_active
    self.ts = ts
    self.act = None
    self.last_updated = {}

  def insert_data(prod_data, cust_data, pandora_box):
    CustThread.prod_data = prod_data
    CustThread.cust_data = cust_data
    CustThread.pandora_box = pandora_box 

  def kill_thread(self):
    self._kill.set()

  def notify(self, ts, prod, act, prod_active=None):
    self._event.set()
    self.ts = ts
    self.prod_active = prod
    self.act = act
    if prod_active:
      self.prod_active.append(prod_active)
  
  def is_done(self):
    return self._work.is_set() == False

  def count_probability(self):
    if len(self.dsl_results) == 0:
      return 0
    else:
      return 1/len(self.dsl_results)

  def process(self):
    prod_values = get_values(CustThread.prod_data, self.prod_active)
    dsl_results = []
    if self.dsl_results:
      for key, value in self.dsl_results.items():
        temp = []
        temp.append(key)
        temp.append([0])
        temp.append(value)
        dsl_results.append(temp)
    self.dsl_results, self.dom_relation = get_dynamic_skyline(dsl_results, self.cust_values, prod_values, self.dom_relation)      
    self.update_pandora_box()

  def update_pandora_box(self):
    CustThread.pandora_box.add_score(list(self.dsl_results.keys()), self.ts, self.count_probability(), self.last_updated)
    for dsl in list(self.dsl_results.keys()):
      self.last_updated[dsl] = [self.ts, self.count_probability()]
      logger.info('Last update 2 pbox[{}] = {}'.format(dsl, self.last_updated.get(dsl)))

  def run(self):
    logger.info('Starting')
    self._work.set()
    if self.prod_active is not None:
      logger.info('Initial dynamic skyline')
      self.process()
    self._work.clear()
    while not self._kill.is_set():
      event = self._event.wait(3)
      if event:
        self._work.set()
        if self.act == 0: 
          logger.info('Product {} in'.format(self.prod_active))
          if not self.dsl_results:
            self.process()
          else:
            self.process()
        elif self.act == 1: 
          logger.info('Product {} out'.format(self.prod_active[0]))
          if self.prod_active[0] in self.dsl_results:
            self.update_pandora_box()
            del self.dsl_results[self.prod_active[0]]
            logger.info('DSL Results: {}'.format(self.dsl_results))
            self.prod_active = get_close_domination(self.dom_relation, self.prod_active[0], self.prod_active[1])
            if self.prod_active:
              self.process()      
        self._event.clear()
        self._work.clear()
      else:
        logger.info('Killed? {}'.format(self._kill.is_set()))  
    logger.info('Exiting')

def get_dynamic_skyline(current_dsl, cust_values, prod_values, dom_relation):
  dsl_results = {}
  prod_values = sorted(prod_values, key=itemgetter(1))
  logger.info('Customer values : {}'.format(cust_values))
  logger.info('Product values sorted : {}'.format(prod_values))
  # calc all diff
  for prod in prod_values:
    prod.append(calc_diff(prod[1], cust_values))
  if not current_dsl:
    dsl_results, dom_relation = compare(prod_values, prod_values, dom_relation)
  else:
    logger.info('Current DSL: {}'.format(current_dsl))
    dsl_results, dom_relation = compare(prod_values, current_dsl, dom_relation)
  logger.info('Close domination relationship: {}'.format(dom_relation))  
  return dsl_results, dom_relation    

def compare(val_a, val_b, dom):
  dsl = {}
  for i in range(0, len(val_a)):
    for j in range(0, len(val_b)):
      logger.info('[P-{}] diff : {} vs [P-{}] diff: {}'.format(val_a[i][0], val_a[i][2], val_b[j][0], val_b[j][2]))
      stat = check_dynamic_domination(val_a[i][2], val_b[j][2])
      if stat == 1:
        val_b[j][1] = [None for x in val_b[j][1]]
        dom = update_domination_relation(dom, val_a[i][0], val_b[j][0])
        logger.info('[P-{}] mendominasi [P-{}]'.format(val_a[i][0], val_b[j][0]))
      elif stat == 2:
        val_a[i][1] = [None for x in val_a[i][1]] 
        dom = update_domination_relation(dom, val_b[j][0], val_a[i][0])
        logger.info('[P-{}] didominasi [P-{}]'.format(val_a[i][0], val_b[j][0]))
      else:
        logger.info('[P-{}] saling mendominasi dengan [P-{}]'.format(val_a[i][0], val_b[j][0]))
  # delete dominated product by None values  
  dsl = delete_dominated_prod(val_a)  
  if val_b != val_a:
    dsl.update(delete_dominated_prod(val_b))
  logger.info('Hasil Dynamic Skyline : {}'.format(dsl))
  return dsl, dom  

def delete_dominated_prod(val):
  dsl = {}
  for i in range(0, len(val)):
    if not all(x == None for x in val[i][1]):
      dsl[val[i][0]] = val[i][2]
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
  prod_active = []
  for key in keys:
    new = []
    new.append(key)
    new.append(data.get_values(key))
    prod_active.append(new)
  return prod_active

def get_close_domination(dom_relation, prod, prod_active):
  dominated = []
  temp = []
  if prod in dom_relation:
    dominated = list(dom_relation.get(prod))
    for dom in dominated:
      for key, value in dom_relation.items():
        if dom != value:
          temp.append(dom)
          break
    logger.info('dominated1 = {}'.format(temp))
    dominated = []    
    for t in temp:
      if t not in prod_active:
        dominated.append(t)
    logger.info('dominated2 = {}'.format(dominated))      
  logger.info('product active now: {}'.format(prod_active))
  logger.info('Close domination: {} - {}'.format(prod, dominated))
  return dominated