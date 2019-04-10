import csv
from collections import OrderedDict
from logging_custom.logging import logger

class Data:
  total_data = 0

  def __init__(self, id, ts_in, ts_out):
    self.id = id
    self.ts_in = ts_in
    self.ts_out = ts_out
    self.values = []
    Data.total_data += 1

  def add_value(self, value=None):
    self.values.append(int(value))

  def count_dimension(self):
    return len(self.values)

  def get_values(self):
    return self.values
    
  def get_data(self):
    return 'ID : {}\tTimestamp : {} - {}\tValues : {}'.format(self.id, self.ts_in, self.ts_out, self.values)

  def get_total_data():
    return Data.total_data

class Product(Data):
  def __init__(self, id, ts_in, ts_out):
    Data.__init__(self, id, ts_in, ts_out)

class Customer(Data):
  def __init__(self, id, ts_in, ts_out):
    Data.__init__(self, id, ts_in, ts_out)    
    self.dsl_results = []
  
  def is_empty(self):
    return self.dsl_results == []

  def add_dsl(self, dsl_result):
    for dsl in dsl_result:
      if not dsl in self.dsl_results:
        self.dsl_results.append(dsl)
        logger.info('[C-{}] Add P-{} (dsl_results : {})'.format(self.id, dsl, self.dsl_results))

  def remove_dsl(self, dsl):
    self.dsl_results.remove(dsl)
    logger.info('[C-{}] Remove P-{} (dsl_results : {})'.format(self.id, dsl, self.dsl_results))

  def get_dsl(self):
    return self.dsl_results

  def get_total_dsl(self):
    return len(self.dsl_results)

  def count_probability(self):
    probability = 1.0/len(self.dsl_results)
    logger.info('[C-{}] Probability: {} (dsl_results : {})'.format(self.id, probability, self.dsl_results))
    return probability

def input_csv(data_name, file, delimiter, event_queue):
  list = [0]
  logger.info('input data {} ({})'.format(data_name, file))
  with open(file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
    for row in csv_reader:
      col_cnt = len(csv_reader.fieldnames)
      id = int(row[csv_reader.fieldnames[0]])
      # instansiasi objek product dan customer 
      if data_name == "product":
        object = Product(id, row[csv_reader.fieldnames[1]], row[csv_reader.fieldnames[2]]) 
      elif data_name == "customer":
        object = Customer(id, row[csv_reader.fieldnames[1]], row[csv_reader.fieldnames[2]])
      # memasukkan objek ke list
      list.append(object)
      # memasukkan value
      for i in range(3, col_cnt):
        list[id].add_value(row[csv_reader.fieldnames[i]])
      # memasukkan event ke queue
      for i in range(0, 2):
        event_queue.enqueue(row[csv_reader.fieldnames[2]] if i == 0 else row[csv_reader.fieldnames[1]], 0 if data_name == "customer" else 1, id, i)
  logger.info('input data {} ({}) selesai'.format(data_name, file))
  return list