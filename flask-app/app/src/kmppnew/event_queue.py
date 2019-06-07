"""
Event Queue Handling
"""

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
    return event[0], event[1], event[2], event[3] 

  def sort_queue(self):
    self.events = sorted(self.events, key=itemgetter(0,3,1,2), reverse=True)

  def get_total_queue(self):
    return len(self.events)

  def get_max_timestamp(self):
    return self.events[0][0]