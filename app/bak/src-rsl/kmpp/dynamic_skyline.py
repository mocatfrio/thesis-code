# import logging

"""
Dynamic Skyline Computation Handling
"""

class DynamicSkyline:
  def __init__(self, product, customer, max_val, pandora_box):
    self.product = product
    self.customer = customer
    self.dim = len(max_val)
  
  def product_out(self, cust_id, ts, prod_id):
    cust_value = self.customer[cust_id]['value']
    # logging.info('\t C-{} | Val: {} | Ts: {}'.format(cust_id, cust_value, ts))
    active_child = None
    try:
      if 'dominating' in self.customer[cust_id]['dsl'][prod_id]:
        active_child = self.find_active_child(self.customer[cust_id]['dsl'][prod_id])
        # logging.info('\t Active child of [P-{}] : {}'.format(prod_id, active_child))
      del self.customer[cust_id]['dsl'][prod_id]
      if active_child:
        self.customer[cust_id]['dsl'] = self.update_dsl(active_child, cust_id, cust_value)
      self.update(cust_id, ts)
    except KeyError:
      pass

  def product_in(self, cust_id, ts, prod_id):
    cust_value = self.customer[cust_id]['value']
    # logging.info('\t C-{} | Val: {} | Ts: {}'.format(cust_id, cust_value, ts))
    self.customer[cust_id]['dsl'] = self.update_dsl(prod_id, cust_id, cust_value)
    self.update(cust_id, ts)

  def customer_in(self, cust_id, ts):
    cust_value = self.customer[cust_id]['value']
    # logging.info('\t C-{} | Val: {} | Ts: {}'.format(cust_id, cust_value, ts))
    prod_id = self.product['active']
    self.customer[cust_id]['dsl'] = self.init_dsl(prod_id, cust_value)
    self.update(cust_id, ts)

  def init_dsl(self, cand, cust_value):
    dsl = {}
    for prod_id in cand:
      dsl[prod_id] = self.calc_diff(cust_value, self.product[prod_id]['value'])
    # logging.info('\t Candidate DSL : {}'.format(dsl))    
    dsl_id = sorted(dsl, key=lambda x: dsl[x]['diff'])
    # logging.info('\t Candidate DSL sorted : {}'.format(dsl_id))
    for i in range(len(dsl_id)):
      if dsl_id[i] is not None:
        for j in range(i + 1, len(dsl_id)):
          if dsl_id[j] is not None:
            if self.is_dominating(dsl[dsl_id[i]], dsl[dsl_id[j]]):
              dsl, dsl_id[j] = self.update_cand(dsl, dsl_id[i], dsl_id[j])
            elif self.is_dominating(dsl[dsl_id[j]], dsl[dsl_id[i]]):
              dsl, dsl_id[i] = self.update_cand(dsl, dsl_id[j], dsl_id[i])
              break
    # logging.info('\t DSL Result : Product {}'.format(list(dsl.keys())))  
    return dsl

  def update_dsl(self, cand, cust_id, cust_value):
    dsl = {}
    for prod_id in cand:
      dsl[prod_id] = self.calc_diff(cust_value, self.product[prod_id]['value'])
    # logging.info('\t Candidate DSL : {}'.format(dsl))
    if 'dsl' in  self.customer[cust_id]:
      dsl.update(self.customer[cust_id]['dsl'])
      # logging.info('\t Candidate DSL + current DSL : {}'.format(dsl))
    dsl_id = sorted(dsl, key=lambda x: dsl[x]['diff'])
    # logging.info('\t Candidate DSL sorted : {}'.format(dsl_id))
    for j in range(len(cand)):
      if cand[j] in dsl_id:
        index = dsl_id.index(cand[j])
        for i in range(len(dsl_id)):
          if dsl_id[index] is not None and dsl_id[i] is not None:
            if i < index:
              if self.is_dominating(dsl[dsl_id[i]], dsl[dsl_id[index]]):
                dsl, dsl_id[index] = self.update_cand(dsl, dsl_id[i], dsl_id[index])
                break
            elif i > index:
              if self.is_dominating(dsl[dsl_id[index]], dsl[dsl_id[i]]):
                dsl, dsl_id[i] = self.update_cand(dsl, dsl_id[index], dsl_id[i])
    # logging.info('\t DSL Result : Product {}'.format(list(dsl.keys()))) 
    return dsl 
  
  def update_cand(self, dsl, psubj_id, pobj_id):
    del dsl[pobj_id]
    if 'dominating' in dsl[psubj_id]:
      if pobj_id not in dsl[psubj_id]['dominating']:
        dsl[psubj_id]['dominating'].append(pobj_id)
    else:
      dsl[psubj_id]['dominating'] = [pobj_id]
    pobj_id = None
    return dsl, pobj_id

  def is_dominating(self, psubj, pobj):
    dominating = 0
    dominated = 0
    for i in range(0, self.dim):
      if psubj['diff'][i] < pobj['diff'][i]:
        dominating += 1
      elif psubj['diff'][i] > pobj['diff'][i]:
        dominated += 1
      else:
        continue
    if dominated == 0 and dominating >= 1:
      return True
    else:
      return False

  def calc_probability(self, dsl_result):
    try:
      return 1.0/len(dsl_result.keys())
    except:
      return 0

  def calc_diff(self, val1, val2):
    res = {}
    res['diff'] = []
    for i in range(0, self.dim):
      res['diff'].append(abs(val1[i] - val2[i]))
    return res

  def find_active_child(self, dsl_result):
    res = []
    # logging.info('\t Dominating : {}'.format(dsl_result['dominating']))  
    # logging.info('\t Product active now : {}'.format(self.product['active']))
    for dom in dsl_result['dominating']:
      if dom in self.product['active']:
        res.append(dom)
    # logging.info('\t Active child = {}'.format(res))      
    return res

  def update(self, cust_id, ts):
    for prod_id in self.customer[cust_id]['dsl']:
      try:
        self.customer[cust_id]['dsl'][prod_id]['ts'] = ts
        self.customer[cust_id]['dsl'][prod_id]['prob'] = self.calc_probability(self.customer[cust_id]['dsl'])
        # logging.info('\t Blm ditambain : Update pbox[p{}] = timestamp: {} | probability: {}'.format(prod_id, self.customer[cust_id]['dsl'][prod_id]['ts'], self.customer[cust_id]['dsl'][prod_id]['prob']))
      except KeyError:
        # logging.info('key error {}'.format(prod_id))
        pass

  def update_history(self, cust_id):
    for prod_id in self.customer[cust_id]['dsl']:
      self.customer[cust_id]['dsl'][prod_id]['last_ts'] = self.customer[cust_id]['dsl'][prod_id]['ts']
      self.customer[cust_id]['dsl'][prod_id]['last_prob'] = self.customer[cust_id]['dsl'][prod_id]['prob']
      # logging.info('\t Udh ditambain : Update pbox[p{}] = timestamp: {} | probability: {}'.format(prod_id, self.customer[cust_id]['dsl'][prod_id]['last_ts'], self.customer[cust_id]['dsl'][prod_id]['last_prob']))
