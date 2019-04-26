import csv

class PandoraBox:
  def __init__(self, total_prod, max_ts):
    self.box = [[0 for col in range(0, max_ts)] for row in range(0, total_prod)]

  def add_score(self, dsl, timestamp, score):
    for id in dsl.keys():
      try:
        last_ts = dsl[id]['last_ts']
      except:
        last_ts = 0
      finally:
        if last_ts > 0:
          self.update_score(id, last_ts, timestamp, dsl[id]['last_prob'])
        if last_ts != timestamp:
          self.box[id][timestamp] += score

  def update_score(self, id, last_ts, now_ts, prob):
    for i in range(last_ts + 1, now_ts):
      self.box[id][i] += prob

  def export_csv(self):
    with open('../dataset/pandora_box.csv', 'w') as csvFile:
      writer = csv.writer(csvFile)
      writer.writerows(self.box)
    csvFile.close()
