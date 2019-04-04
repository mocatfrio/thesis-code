import logging

class PandoraBox:
  def __init__(self, total_product, max_timestamp):
    self.box = [[0 for col in range(0, max_timestamp)] for row in range(0, total_product)]

  def add_score(self, dsl, timestamp, score):
    logging.debug('dsl = {}'.format(dsl))
    for product_id in range(0, len(dsl)):
      self.box[dsl[product_id]][timestamp] += score
      logging.debug('Insert PandoraBox [{}][{}] + {} = {}'. format(dsl[product_id], timestamp, score, self.box[dsl[product_id]][timestamp]))

  def get_pandora_box(self):
    return self.box