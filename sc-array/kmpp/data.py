import csv
from collections import OrderedDict
# from .logging import logger

class Data:
  def __init__(self):
    self.data = {}

  def add_data(self, id, ts_in, ts_out):
    self.data[id] = [ts_in, ts_out]

  def add_value(self, id, value):
    self.data[id].append(value)
    # logger.info('ID : {}\tTimestamp : {} - {}\tValues : {}'.format(id, self.data.get(id)[0], self.data.get(id)[1], self.data.get(id)[2])) 
    
  def get_total_data(self):
    return len(self.data)
  
  def get_values(self, id):
    return self.data.get(id)[2]

def input_csv(type, file, event_queue, data_obj):
  # logger.info('input data ({})'.format(file))
  with open(file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
      values = []
      col_cnt = len(csv_reader.fieldnames)
      # insert data
      data_obj.add_data(int(row[csv_reader.fieldnames[0]]), int(row[csv_reader.fieldnames[1]]), int(row[csv_reader.fieldnames[2]])) 
      # insert value
      for i in range(3, col_cnt):
        values.append(int(row[csv_reader.fieldnames[i]]))
      data_obj.add_value(int(row[csv_reader.fieldnames[0]]), values)
      # insert event to the queue
      for i in range(0, 2):
        event_queue.enqueue(int(row[csv_reader.fieldnames[1]]) if i == 0 else int(row[csv_reader.fieldnames[2]]), 0 if type == 'p' else 1, int(row[csv_reader.fieldnames[0]]), i)
  # logger.info('input data ({}) selesai'.format(file))