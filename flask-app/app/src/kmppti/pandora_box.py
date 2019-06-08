"""
Pandora Box Handling
"""

import csv 
from app import app

class PandoraBox:
  def __init__(self, total_prod=None, max_ts=None):
    try:
      self.box = [[0 for col in range(0, max_ts)] for row in range(0, total_prod)]
    except:
      self.box = []

  def update(self, dsl):
    for p in dsl:
      if 'last_ts' in dsl[p] and 'last_prob' in dsl[p]:
        if dsl[p]['ts'] > dsl[p]['last_ts']:
          self.update_score(p, dsl[p]['ts'], dsl[p]['last_ts'], dsl[p]['prob'], dsl[p]['last_prob'])
      else:
        self.box[p][dsl[p]['ts']] += dsl[p]['prob']

  def update_score(self, p, ts, last_ts, prob, last_prob):
    for i in range(last_ts + 1, ts):
      self.box[p][i] += last_prob
    self.box[p][ts] += prob

  def insert_score(self, prod_score):
    self.box.append(prod_score)
  
  def get_score(self, prod_id, ts_start, ts_end):
    total_score = 0
    try:
      for i in range(ts_start, ts_end + 1):
        total_score += self.box[prod_id][i]
    except:
      print('out of list')
    finally:
      return total_score

  def export_csv(self, pandora_path):
    with open(pandora_path + '/pandora_box.csv', 'w') as csvFile:
      writer = csv.writer(csvFile)
      writer.writerows(self.box)
    csvFile.close()
