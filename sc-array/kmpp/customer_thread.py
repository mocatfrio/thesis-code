import threading
from operator import itemgetter
# from .logging import logger

class CustThread(threading.Thread):
  prod_data = None
  cust_data = None
  pandora_box = None

  def __init__(self, cust_id, timestamp, prod_active):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._event = threading.Event()
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

  def notify(self, timestamp, product, act, prod_active=None):
    if not self._kill.is_set():
      self._event.set()
      self.timestamp = timestamp
      self.product = product
      self.act = act
      if prod_active is not None:
        self.prod_active = prod_active

  def get_last_event(self):
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

  def init_dynamic_skyline(self):
    if self.prod_active:
      # logger.info("========================================================================")          
      # logger.info('Initial dynamic skyline')
      self.process(self.prod_active)
    self.last_event = 0
  
  def process_product_in(self):
    # logger.info("========================================================================")
    # logger.info('Product {} in, ts: {}'.format(self.product, self.timestamp))
    self.process(self.product)
    self.last_event = 'p' + str(self.product[0]) + 'i'

  def process_product_out(self):
    # logger.info("========================================================================")            
    # logger.info('Product {} out, ts: {}'.format(self.product, self.timestamp))
    # cek jika product out adalah dsl
    index = check(self.product, self.dsl_results)
    # jika product out adalah dsl
    if index is not None:
      # update pandora
      if list(self.last_updated.get(self.product[0]))[0] != self.timestamp:
        self.update_pandora_box()    
      # hapus dsl result dan last updated
      del self.dsl_results[index]
      del self.last_updated[self.product[0]]
      # jika product out pernah mendominasi produk lain
      if self.product[0] in self.dom_relation:
        close_dominated = get_close_domination(self.dom_relation, self.product[0], self.prod_active)
        self.process(close_dominated)
    self.last_event = 'p' + str(self.product[0]) + 'o'
  
  def process_kill(self):
    # logger.info("========================================================================")    
    # logger.info('{} killed..., ts: {}'.format(self.name, self.timestamp))
    self.update_pandora_box()
    self.last_event = 1

  def process(self, arg):
    # ambil nilai
    prod_values = get_values(CustThread.prod_data, arg)     
    # cari dynamic skyline
    self.dsl_results, self.dom_relation = get_dynamic_skyline(self.dsl_results, self.cust_values, prod_values, self.dom_relation)      
    # update pandora box
    self.update_pandora_box()

  def update_pandora_box(self):
    # masukkan score ke pandora box
    CustThread.pandora_box.add_score(self.dsl_results, self.timestamp, self.count_probability(), self.last_updated)
    # update last updated
    if not self._kill.is_set():
      for dsl in self.dsl_results:
        self.last_updated[dsl[0]] = [self.timestamp, self.count_probability()]
        # logger.info('Last update 2 pbox[{}] = {}'.format(dsl[0], self.last_updated.get(dsl[0])))

  def run(self):
    # logger.info('{} starting..., ts: {}'.format(self.name, self.timestamp))
    # thread init
    self.init_dynamic_skyline()
    while not self._kill.is_set():
      if self._kill.is_set():
        break
      else:
        event = self._event.wait(3)
        if event:
          # product in
          if self.act == 0: 
            self.process_product_in()
          # product out          
          elif self.act == 1: 
            self.process_product_out()
          # thread killed
          elif self.act == 2:
            self.process_kill()
          self._event.clear()
    # logger.info('{} exiting'.format(self.name))

def get_dynamic_skyline(current_dsl, cust_values, prod_values, dom_relation):
  prod_values = sorted(prod_values, key=itemgetter(1))
  # logger.info('Customer values : {}'.format(cust_values))
  # logger.info('Product values  : {}'.format(prod_values))
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
  # logger.info('Close domination relationship: {}'.format(dom_relation))  
  return dsl_results, dom_relation    

def compare(val_a, val_b, dom):
  for i in range(0, len(val_a)):
    for j in range(0, len(val_b)):
      # logger.info('[P-{}] diff : {} vs [P-{}] diff: {}'.format(val_a[i][0], val_a[i][1], val_b[j][0], val_b[j][1]))
      stat = check_dynamic_domination(val_a[i][1], val_b[j][1])
      if stat == 1:
        val_b[j][2] = 1
        dom = update_domination_relation(dom, val_a[i][0], val_b[j][0])
        # logger.info('[P-{}] mendominasi [P-{}]'.format(val_a[i][0], val_b[j][0]))
      elif stat == 2:
        val_a[i][2] = 1
        dom = update_domination_relation(dom, val_b[j][0], val_a[i][0])
        # logger.info('[P-{}] didominasi [P-{}]'.format(val_a[i][0], val_b[j][0]))
      else:
        pass
        # logger.info('[P-{}] saling mendominasi dengan [P-{}]'.format(val_a[i][0], val_b[j][0]))
  dsl = get_dsl_result(val_a)  
  if val_b != val_a:
    dsl.extend(get_dsl_result(val_b))
  # logger.info('DSL Result : {}'.format(dsl))
  return dsl, dom  

def get_dsl_result(val):
  dsl = []
  for i in range(0, len(val)):
    # ambil yg flagnya 0, artinya ga didominasi samsek
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
  # logger.info('dom relation dict = {}'.format(dom_relation))  
  close_dominated = list(dom_relation.get(prod)) 
  # logger.info('close dominated (1) = {}'.format(close_dominated))
  del dom_relation[prod]
  # convert dict to list
  dom_rel = []
  for value in dom_relation.values():
    dom_rel.append(value)
  # logger.info('dom relation array = {}'.format(dom_rel))
  # cari produk yang hanya didominasi oleh dia
  for close_dom in close_dominated:
    for dom in dom_rel:
      for d in dom:
        if close_dom == d:
          close_dominated.remove(close_dom)
  # logger.info('close dominated (2) = {}'.format(close_dominated))
  # cari yang masih aktif 
  new_close_dom = []
  for close_dom in close_dominated:
    if close_dom in prod_active:
      new_close_dom.append(close_dom)
  # logger.info('product active now: {}'.format(prod_active))
  # logger.info('close dominated (3) = {}'.format(new_close_dom))      
  # logger.info('Close domination: {} - {}'.format(prod, new_close_dom))
  return new_close_dom

def check(val, array):
  for i in range(0, len(array)):
    if array[i][0] == val[0]:
      return i
  return None