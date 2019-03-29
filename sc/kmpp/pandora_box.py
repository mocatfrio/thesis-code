class PandoraBox:
  def __init__(self):
    self.box = []

  def add_score(self, product_id, event_id, score):
    self.box[product_id][event_id] = score