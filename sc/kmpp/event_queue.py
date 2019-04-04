import logging
from operator import itemgetter

class EventQueue:
  def __init__(self):
    self.events = []

  def is_empty(self):
    return self.events == []

  def enqueue(self, timestamp, owner, owner_id, action):
    self.event = []
    self.event.append(int(timestamp))
    self.event.append(int(owner)) 
    self.event.append(int(owner_id)) 
    self.event.append(int(action))
    self.events.append(self.event)

  def dequeue(self):
    return self.events.pop()

  def sort_queue(self):
    self.events = sorted(self.events, key=itemgetter(0,3,1,2), reverse=True)

  def get_queue(self):
    return self.events

  def get_total_queue(self):
    return len(self.events)

  def get_max_timestamp(self):
    return self.events[0][0]