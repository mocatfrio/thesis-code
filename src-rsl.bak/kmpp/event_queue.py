# import logging
from operator import itemgetter

class EventQueue:
  def __init__(self):
    self.events = []

  def is_empty(self):
    return self.events == []

  def enqueue(self, timestamp, owner, owner_id, action):
    self.event = [timestamp, owner, owner_id, action]
    self.events.append(self.event)

  def dequeue(self):
    event = self.events.pop()
    # logging.info('Event : {}'.format(event))
    return event[0], event[1], event[2], event[3] 

  def sort_queue(self):
    """
    sort priority:
    1. timestamp
    2. action (in = 0, out = 1)
    3. type (p = 0, c = 1)
    4. id
    """
    self.events = sorted(self.events, key=itemgetter(0,3,1,2), reverse=True)
    # logging.info('Sorted Queue')
    # for event in self.events:
      # logging.info('\t {}'.format(event))

  def get_total_queue(self):
    return len(self.events)

  def get_max_timestamp(self):
    return self.events[0][0]