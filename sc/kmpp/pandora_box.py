from logging_custom.logging import logger

class PandoraBox:
  def __init__(self, total_prod, max_ts):
    self.box = [[0 for col in range(0, max_ts)] for row in range(0, total_prod)]
    self.recent_ts = [0] * total_prod

  def add_score(self, dsl, ts, score):
    self.fill_score(dsl, ts-1)
    logger.info('Add score | DSL = {}'.format(dsl))
    for i in range(0, len(dsl)):
      prod_id = dsl[i]
      self.box[prod_id][ts] += score
      logger.info('Insert PandoraBox [{}][{}] + {} = {}'. format(prod_id, ts, score, self.box[prod_id][ts]))
      self.recent_ts[prod_id] = ts 
      logger.info('Recent timestamp [P-{}] : {}'. format(prod_id, self.recent_ts[prod_id]))

  def get_pandora_box(self):
    return self.box

  def fill_score(self, dsl, ts):
    logger.info('Fill score | DSL = {}'.format(dsl))
    for i in range(0, len(dsl)):
      prod_id = dsl[i]
      current_score = self.box[prod_id][self.recent_ts[prod_id]]
      logger.info('Current Score [P-{}] : {}'.format(prod_id, current_score))
      for j in range(self.recent_ts[prod_id] + 1, ts + 1):
        self.box[prod_id][j] += current_score
        logger.info('Insert PandoraBox [{}][{}] + {} = {}'. format(prod_id, j, current_score, self.box[prod_id][j]))
      self.recent_ts[prod_id] = ts 
      logger.info('Recent timestamp [P-{}] : {}'. format(prod_id, self.recent_ts[prod_id]))

    