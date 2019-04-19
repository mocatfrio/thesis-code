from .logging import logger

class PandoraBox:
  def __init__(self, total_prod, max_ts):
    self.box = [[0 for col in range(0, max_ts)] for row in range(0, total_prod)]
    for i in range(1, len(self.box)):
      self.box[i][0] = i
    for i in range(1, len(self.box[0])):
      self.box[0][i] = i

  def add_score(self, dsl, ts, score, last_updated):
    for i in range(0, len(dsl)):
      id = dsl[i][0]
      try:
        last_ts = list(last_updated.get(id))[0]
        logger.info('Last update 1 pbox[{}] = {}'.format(id, list(last_updated.get(id))))
      except:
        last_ts = 0
        logger.info('Last update 1 pbox[{}] = {}'.format(id, last_ts))
      finally:
        if last_ts > 0:
          self.update_score(id, last_ts, ts, list(last_updated.get(id))[1])
        if last_ts != ts:
          self.box[id][ts] += score
          logger.info('Add score pbox[{}][{}] + {} = {}'. format(id, ts, score, self.box[id][ts]))

  def update_score(self, id, last_ts, now_ts, prob):
    for i in range(last_ts + 1, now_ts):
      self.box[id][i] += prob
      logger.info('Update score pbox[{}][{}] + {} = {}'.format(id, i, prob, self.box[id][i]))

  def display(self):
    logger.info('Pandora Box')
    for row in self.box:
      logger.info(row)
