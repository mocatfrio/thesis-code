"""
Reverse Skyline Computation Handling
"""

class ReverseSkyline:
  def __init__(self, product, customer, dim):
    self.product = product['data']
    self.customer = customer['data']
    self.product_active = product['active']
    self.customer_active = customer['active']
    self.dim = dim
    self.define_orthant()

  def compute(self, pid):
    self.my_id = pid
    self.my_value = self.product[pid]['value']
    self.find_midpoint_skyline()
    return self.find_reverse_skyline()

  def define_orthant(self):
    self.orthant = {}
    for i in range(2**self.dim): 
      id = format(i, '#0{}b'.format(self.dim + 2))[2:]
      self.orthant[id] = {}
  
  def get_orthant_area(self, product_val):
    res = []
    for i in range(self.dim):
      if product_val[i] <= self.my_value[i]:
        res.append('0')
      else:
        res.append('1')
    res = ''.join(res)
    return res

  def find_midpoint_skyline(self):
    for pid in self.product_active:
      if pid != self.my_id:
        midpoint = self.calc_midpoint(self.my_value, self.product[pid]['value'])
        area = self.get_orthant_area(self.product[pid]['value'])
        if not self.orthant[area]:
          self.orthant[area][pid] = midpoint
        else:
          self.orthant[area] = self.update_midskyline(self.orthant[area], midpoint, pid)
 
  def find_reverse_skyline(self):
    rsl = []
    for cid in self.customer_active:
      area = self.get_orthant_area(self.customer[cid]['value'])
      if not self.orthant[area]:
        rsl.append(cid)
      else:
        dom = 0
        for i in self.orthant[area]:
          if self.is_dominating(self.orthant[area][i], self.customer[cid]['value']):
            dom += 1
        if dom == 0:
          rsl.append(cid)
    return rsl

  def update_midskyline(self, msl, cand, cand_id):
    res = {}
    for i in msl:
      if self.is_dominating(cand, msl[i]):
        res[cand_id] = cand
      else:
        res[i] = msl[i]
        if not self.is_dominating(msl[i], cand):
          res[cand_id] = cand
    return res
  
  def is_dominating(self, subject, target):
    dominating = 0
    dominated = 0
    for i in range(0, self.dim):
      subj_diff = abs(self.my_value[i] - subject[i])
      target_diff = abs(self.my_value[i] - target[i])
      if subj_diff == target_diff:
        continue
      elif subj_diff < target_diff:
        dominating += 1
      elif subj_diff > target_diff:
        dominated += 1
    if dominated == 0 and dominating >= 1:
      return True
    else:
      return False

  def calc_midpoint(self, val1, val2):
    res = []
    for i in range(self.dim):
      res.append((val1[i] + val2[i])/2)
    return res