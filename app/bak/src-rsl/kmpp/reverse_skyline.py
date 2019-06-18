# import logging

class ReverseSkyline:
  def __init__(self, product, customer, max_val):
    self.product = product
    self.customer = customer
    self.dim = len(max_val)
    self.max_val = max_val
    self.define_orthant()

  def compute(self, prod_id):
    self.my_id = prod_id
    self.my_value = self.product[prod_id]['value']
    # self.print_orthant(0)
    self.find_midpoint_skyline()
    # self.print_orthant(1)
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
    for id in self.product['active']:
      if id != self.my_id:
        midpoint = self.calc_midpoint(self.my_value, self.product[id]['value'])
        area = self.get_orthant_area(self.product[id]['value'])
        if not self.orthant[area]:
          self.orthant[area][id] = midpoint
        else:
          self.orthant[area] = self.update_midskyline(self.orthant[area], midpoint, id)
 
  def find_reverse_skyline(self):
    rsl = []
    for id in self.customer['active']:
      area = self.get_orthant_area(self.customer[id]['value'])
      if not self.orthant[area]:
        rsl.append(id)
      else:
        dom = 0
        for i in self.orthant[area]:
          if self.is_dominating(self.orthant[area][i], self.customer[id]['value']):
            dom += 1
        if dom == 0:
          rsl.append(id)
    # logging.info('\t RSL Result : Customer {}'.format(rsl))
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

  # def print_orthant(self, i):
  #   if i == 0:
      # logging.info('\t MSL before : {}'.format(self.orthant))
    # else:
      # logging.info('\t MSL after : {}'.format(self.orthant))