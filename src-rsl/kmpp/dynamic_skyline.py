import logging

"""
Dynamic Skyline Computation Handling
"""

class DynamicSkyline:
  def __init__(self, product, customer, max_val, pandora_box):
    self.product = product
    self.customer = customer
    self.dim = len(max_val)
    self.pandora_box = pandora_box

  def _define_cust(self, id):
    self.my_id = id
    self.my_value = self.customer[id]['value']
    logging.info('C-{} : {}'.format(self.my_id, self.my_value))

  def start_computation(self, id, ts, act=None, product_id=None):
    self._define_cust(id)
    self.ts = ts
    if product_id is None:
      logging.info('Initial dynamic skyline')
      product_id = self.product['active']
    if product_id:
      if act is None or act == 0:
        self.customer[self.my_id]['dsl'] = self.product_in(product_id)
      elif act == 1:
        self.customer[self.my_id]['dsl'] = self.product_out(self.customer[self.my_id]['dsl'], product_id)
      elif act == 2:
        self.update_pandora_box(self.customer[self.my_id]['dsl'])

  def product_out(self, dsl_result, product_id):
    if product_id in dsl_result:
      if dsl_result[product_id]['last_ts'] != self.ts:
        self.update_pandora_box(self.customer[self.my_id]['dsl'])
      active_child = None
      if 'dominating' in dsl_result[product_id]:
        active_child = self.find_active_child(dsl_result[product_id])
        logging.info('Active child of [P-{}] : {}'.format(product_id, active_child))
      del dsl_result[product_id]
      if active_child:
        dsl_result = self.product_in(active_child)
    return dsl_result
  
  def product_in(self, candidate):
    dsl_result = {}
    dsl_result = self.find_dynamic_skyline(candidate)
    self.update_pandora_box(dsl_result)
    return dsl_result

  def find_dynamic_skyline(self, candidate):
    dsl_cand = {}
    if isinstance(candidate, list):
      for id in candidate:
        dsl_cand[id] = {}
        dsl_cand[id]['diff'] = self.calc_diff(self.my_value, self.product[id]['value'])
    else:
      dsl_cand[candidate] = {}
      dsl_cand[candidate]['diff'] = self.calc_diff(self.my_value, self.product[candidate]['value'])
    logging.info('Candidate DSL : {}'.format(dsl_cand))
    if 'dsl' in  self.customer[self.my_id]:
      dsl_cand.update(self.customer[self.my_id]['dsl'])
      logging.info('Candidate DSL + current DSL : {}'.format(dsl_cand))
    cand_id = sorted(dsl_cand, key=lambda x: dsl_cand[x]['diff'])
    logging.info('Candidate DSL sorted : {}'.format(cand_id))
    if isinstance(candidate, list):
      # init dynamic skyline
      for i in range(len(cand_id)):
        if cand_id[i] is None:
          continue
        for j in range(i + 1, len(cand_id)):
          if cand_id[j] is None:
            continue
          dsl_cand, cand_id[j] = self.check_domination(cand_id[i], cand_id[j], dsl_cand)
    else:
      # single candidate 
      index = cand_id.index(candidate)
      for i in range(len(cand_id)):
        if cand_id[index] is None:
          break
        if i < index:
          dsl_cand, cand_id[index] = self.check_domination(cand_id[i], cand_id[index], dsl_cand)
        elif i > index:
          dsl_cand, cand_id[index] = self.check_domination(cand_id[index], cand_id[i], dsl_cand)
        else:
          continue
    logging.info('DSL Result : {}'.format(dsl_cand))  
    return dsl_cand 
  
  def check_domination(self, subject_id, target_id, dsl_cand):
    if self.is_dominating(dsl_cand[subject_id]['diff'], dsl_cand[target_id]['diff']):
      del dsl_cand[target_id]  
      dsl_cand[subject_id] = self.update_dict(dsl_cand[subject_id], 'dominating', target_id)
      target_id = None
    return dsl_cand, target_id

  def is_dominating(self, subject, target):
    dominating = 0
    dominated = 0
    for i in range(0, self.dim):
      if subject[i] == target[i]:
        continue
      elif subject[i] < target[i]:
        dominating += 1
      else:
        dominated += 1
    if dominated == 0 and dominating >= 1:
      return True
    else:
      return False
  
  def update_dict(self, my_dict, key, val):
    if key == 'last_ts' or key == 'last_prob':
      my_dict[key] = val
    elif key == 'dominating':
      if key in my_dict:
        if val not in my_dict[key]:
          my_dict[key].append(val)
      else:
        my_dict[key] = [val]
    return my_dict

  def update_pandora_box(self, dsl_result):
    self.pandora_box.add_score(dsl_result, self.ts, self.calc_probability(dsl_result))
    # update last ts and last prob
    for id in dsl_result:
      dsl_result[id] = self.update_dict(dsl_result[id], 'last_ts', self.ts)
      dsl_result[id] =  self.update_dict(dsl_result[id], 'last_prob', self.calc_probability(dsl_result))
      logging.info('Last update 2 pbox[{}] = timestamp: {} | probability: {}'.format(id, dsl_result[id]['last_ts'], dsl_result[id]['last_prob']))

  def calc_probability(self, dsl_result):
    try:
      return 1.0/len(dsl_result.keys())
    except:
      return 0

  def calc_diff(self, val1, val2):
    res = []
    for i in range(0, self.dim):
      res.append(abs(val1[i] - val2[i]))
    return res

  def find_active_child(self, dsl_result):
    res = []
    logging.info('Dominating : {}'.format(dsl_result['dominating']))  
    logging.info('Product active now : {}'.format(self.product['active']))
    for dom in dsl_result['dominating']:
      if dom in self.product['active']:
        res.append(dom)
    logging.info('Active child = {}'.format(res))      
    return res