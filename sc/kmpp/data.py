import logging
import csv
from collections import OrderedDict

class Data:
  total_data = 0

  def __init__(self, id=None, timestamp_in=None, timestamp_out=None):
    self.id = id
    self.timestamp_in = timestamp_in
    self.timestamp_out = timestamp_out
    self.values = []
    Data.total_data += 1

  def add_value(self, value=None):
    self.values.append(int(value))

  def count_dimension(self):
    return len(self.values)
    
  def get_data(self):
    return 'ID : {}\tTimestamp : {} - {}\tValues : {}'.format(self.id, self.timestamp_in, self.timestamp_out, self.values)

  def get_total_data():
    return Data.total_data

class Product(Data):
  def __init__(self, id, timestamp_in, timestamp_out):
    Data.__init__(self, id, timestamp_in, timestamp_out)

class Customer(Data):
  def __init__(self, id, timestamp_in, timestamp_out):
    Data.__init__(self, id, timestamp_in, timestamp_out)    
    self.dsl_results = []
  
  def is_empty(self):
    return self.dsl_results == []

  def add_dsl(self, dsl_result):
    for dsl in dsl_result:
      self.dsl_results.append(dsl)
      logging.debug('[C-{}] Adding P-{} (dsl_results : {})'.format(self.id, dsl, self.dsl_results))
    # self.dsl_results = list(OrderedDict.fromkeys(self.dsl_results))

  def remove_dsl(self, dsl):
    self.dsl_results.remove(dsl)
    logging.debug('[C-{}] Removing P-{} (dsl_results : {})'.format(self.id, dsl, self.dsl_results))

  def get_total_dsl(self):
    return len(self.dsl_results)

  def count_probability(self):
    probability = 1.0/len(self.dsl_results)
    logging.debug('[C-{}] Probability: {} (dsl_results : {})'.format(self.id, probability, self.dsl_results))
    return probability

def input_csv(data_name, file, delimiter, event_queue):
  list = []
  row_count = 0

  logging.debug('input data {} ({})'.format(data_name, file))
  with open(file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
    for row in csv_reader:
      col_count = len(csv_reader.fieldnames)
      
      # instansiasi objek product dan customer 
      if data_name == "product":
        object = Product(row[csv_reader.fieldnames[0]], row[csv_reader.fieldnames[1]], row[csv_reader.fieldnames[2]]) 
      elif data_name == "customer":
        object = Customer(row[csv_reader.fieldnames[0]], row[csv_reader.fieldnames[1]], row[csv_reader.fieldnames[2]])
      
      # memasukkan objek ke list
      list.append(object)
      
      # memasukkan value
      for i in range(3,col_count):
        list[row_count].add_value(row[csv_reader.fieldnames[i]])
      row_count += 1

      # memasukkan event ke queue
      for j in range(0,2):
        event_queue.enqueue(row[csv_reader.fieldnames[2]] if j == 0 else row[csv_reader.fieldnames[1]], 0 if data_name == "customer" else 1, row[csv_reader.fieldnames[0]], j)
  
  logging.debug('input data {} ({}) selesai'.format(data_name, file))
  return list
