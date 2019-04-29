import threading
from operator import itemgetter
from .custom_logger import logger

class CustThread(threading.Thread):
  data = {}
  pandora_box = None

  def __init__(self, cust_id, timestamp, prod_active):
    threading.Thread.__init__(self)
    self._kill = threading.Event()
    self._event = threading.Event()
    self.id = cust_id
    self.name = "thread_c" + str(cust_id)
    self.timestamp = timestamp
    self.cust_value = CustThread.data['customer'][cust_id]['value']
    self.dsl_result = {}
    self.prod_active = prod_active
    self.input = {}
    self.last_event = None

  def notify(self, timestamp, product, act, prod_active=None):
    if not self._kill.is_set():
      self._event.set()
      self.timestamp = timestamp
      self.input['product'] = product
      self.input['act'] = act
      if prod_active:
        self.prod_active = prod_active

  def get_last_event(self):
    return self.last_event

  def kill_thread(self, timestamp):
    self._event.set()
    self.timestamp = timestamp
    self.input['act'] = 2
    self._kill.set()

  def count_probability(self):
    try:
      return 1.0/len(self.dsl_result.keys())
    except:
      return 0

  def process(self, prod_id):
    prod_value = get_value(CustThread.data['product'], prod_id)     
    self.dsl_result = find_dynamic_skyline(self.dsl_result, self.cust_value, prod_value)      
    self.update_pandora_box()

  def update_pandora_box(self):
    CustThread.pandora_box.add_score(self.dsl_result, self.timestamp, self.count_probability())
    if not self._kill.is_set():
      for dsl in self.dsl_result:
        self.dsl_result[dsl] = update_dict(self.dsl_result[dsl], 'last_ts', self.timestamp)
        self.dsl_result[dsl] = update_dict(self.dsl_result[dsl], 'last_prob', self.count_probability())
        logger.info('Last update 2 pbox[{}] = timestamp: {} | probability: {}'.format(dsl, self.dsl_result[dsl]['last_ts'], self.dsl_result[dsl]['last_prob']))

  def init_dynamic_skyline(self):
    if self.prod_active:
      logger.info("========================================================================")
      logger.info('Initial dynamic skyline')
      self.process(self.prod_active)
    self.last_event = 0
  
  def process_product_in(self):
    logger.info("========================================================================")
    logger.info('Product {} in, ts: {}'.format(self.input['product'], self.timestamp))
    self.process(self.input['product'])
    self.last_event = 'p' + str(self.input['product']) + 'i'

  def process_product_out(self):
    logger.info("========================================================================")
    logger.info('Product {} out, ts: {}'.format(self.input['product'], self.timestamp))
    if self.input['product'] in self.dsl_result:
      if self.dsl_result[self.input['product']]['last_ts'] != self.timestamp:
        self.update_pandora_box()
      active_child = None
      if 'dominating' in self.dsl_result[self.input['product']]:
        active_child = get_active_child(self.dsl_result[self.input['product']], self.prod_active)
        logger.info('Active child of [P-{}] : {}'.format(self.input['product'], active_child))
      del self.dsl_result[self.input['product']]
      if active_child:
        self.process(active_child)
    self.last_event = 'p' + str(self.input['product']) + 'o'
  
  def process_kill(self):
    logger.info("========================================================================")    
    logger.info('{} killed..., ts: {}'.format(self.name, self.timestamp))
    self.update_pandora_box()
    self.last_event = 1

  def run(self):
    logger.info('{} starting..., ts: {}'.format(self.name, self.timestamp))
    self.init_dynamic_skyline()
    while not self._kill.is_set():
      if self._kill.is_set():
        break
      else:
        event = self._event.wait(3)
        if event:
          if self.input['act'] == 0: 
            self.process_product_in()
          elif self.input['act'] == 1: 
            self.process_product_out()
          elif self.input['act'] == 2:
            self.process_kill()
          self._event.clear()
    logger.info('{} exiting'.format(self.name))

def find_dynamic_skyline(current_dsl, cust_value, prod_value):
  logger.info('Customer value : {}'.format(cust_value))
  for id in prod_value.keys():
    prod_value[id]['diff'] = calc_diff(prod_value[id]['value'], cust_value)
  logger.info('Product value : {}'.format(prod_value))  
  logger.info('Current DSL : {}'.format(current_dsl))  
  current_dsl.update(prod_value)
  logger.info('Current DSL + Product value : {}'.format(current_dsl))  
  dsl_cand = sorted(current_dsl, key=lambda x: (current_dsl[x]['diff']))
  logger.info('Current DSL sorted : {}'.format(dsl_cand))  
  if len(prod_value) == 1:
    index = dsl_cand.index(list(prod_value.keys())[0])
    for i in range(0, index):
      if is_dominating(current_dsl[dsl_cand[i]], current_dsl[dsl_cand[index]]):
        current_dsl, dsl_cand[index] = update_cand(dsl_cand[i], dsl_cand[index], current_dsl)
        break
    if dsl_cand[index] is not None:
      for i in range(index+1, len(dsl_cand)):
        if is_dominating(current_dsl[dsl_cand[index]], current_dsl[dsl_cand[i]]):
          current_dsl, dsl_cand[i] = update_cand(dsl_cand[index], dsl_cand[i], current_dsl)
  else:
    for i in range(0, len(dsl_cand)):
      if dsl_cand[i] is None:
        continue
      for j in range(i+1, len(dsl_cand)):
        if dsl_cand[j] is None:
          continue
        if is_dominating(current_dsl[dsl_cand[i]], current_dsl[dsl_cand[j]]):
          current_dsl, dsl_cand[j] = update_cand(dsl_cand[i], dsl_cand[j], current_dsl)
  logger.info('DSL Result : {}'.format(current_dsl))    
  return current_dsl    

def is_dominating(subject, target):
  dim = len(subject['diff'])
  dominating = 0
  dominated = 0
  for i in range(0, dim):
    if list(subject['diff'])[i] == list(target['diff'])[i]:
      continue
    elif list(subject['diff'])[i] < list(target['diff'])[i]:
      dominating += 1
    else:
      dominated += 1
  if dominated == 0 and dominating >= 1:
    return True
  else:
    return False
  
def update_cand(p_dominating, p_dominated, current_dsl):
  del current_dsl[p_dominated]  
  current_dsl[p_dominating] = update_dict(current_dsl[p_dominating], 'dominating', p_dominated)
  p_dominated = None
  return current_dsl, p_dominated
  
def update_dict(my_dict, key, val):
  if key == 'last_ts' or key == 'last_prob':
    my_dict[key] = val
  else:
    if key in my_dict:
      if val not in my_dict[key]:
        my_dict[key].append(val)
    else:
      my_dict[key] = [val]
  return my_dict

def calc_diff(val1, val2):
  diff = []
  for col in range(0, len(val1)):
    diff.append(abs(val1[col] - val2[col]))
  return diff

def get_value(data, prod_id):
  prod_value = {}
  if not isinstance(prod_id, list):
    prod_id = [prod_id]
  for id in prod_id:
    prod_value[id] = {}
    prod_value[id]['value'] = data[id]['value']
  return prod_value

def get_active_child(dsl, prod_active):
  active = []
  logger.info('Dominating : {}'.format(dsl['dominating']))  
  logger.info('Product active now : {}'.format(prod_active))
  for dom in dsl['dominating']:
    if dom in prod_active:
      active.append(dom)
  logger.info('Active child = {}'.format(active))      
  return active