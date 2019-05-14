import csv, logging

class PandoraBox:
  def __init__(self, total_prod=None, max_ts=None):
    try:
      self.box = [[0 for col in range(0, max_ts)] for row in range(0, total_prod)]
    except:
      self.box = []

  def insert_score(self, prod_score):
    self.box.append(prod_score)

  def add_score(self, dsl, timestamp, score):
    for id in list(dsl.keys()):
      try:
        last_ts = dsl[id]['last_ts']
      except:
        last_ts = 0
      finally:
        logging.info('Last update 1 pbox[{}] = {}'.format(id, last_ts))
        if last_ts > 0:
          self.update_score(id, last_ts, timestamp, dsl[id]['last_prob'])
        if last_ts != timestamp:
          self.box[id][timestamp] += score
          logging.info('Add score pbox[{}][{}] + {} = {}'. format(id, timestamp, score, self.box[id][timestamp]))

  def update_score(self, id, last_ts, now_ts, prob):
    for i in range(last_ts + 1, now_ts):
      self.box[id][i] += prob
      logging.info('Update score pbox[{}][{}] + {} = {}'.format(id, i, prob, self.box[id][i]))

  def print_box(self):
    logging.info('Pandora Box')
    for row in self.box:
      logging.info(row)
  
  def get_score(self, prod_id, ts_start, ts_end):
    total_score = 0
    try:
      for i in range(ts_start, ts_end + 1):
        total_score += self.box[prod_id][i]
    except:
      print('out of list')
    finally:
      return total_score

  def export_csv(self):
    with open('pandora_box.csv', 'w') as csvFile:
      writer = csv.writer(csvFile)
      writer.writerows(self.box)
    csvFile.close()
    logging.info('pandora box csv exported succesfully')
