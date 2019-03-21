import csv
import threading
import time
import trace
import sys

class Data:
  data_count = 0

  def __init__(self, id=None, timestamp_in=None, timestamp_out=None):
    self.id = id
    self.timestamp_in = timestamp_in
    self.timestamp_out = timestamp_out
    self.values = []
    self.dimension = 0
    Data.data_count += 1

  def addValue(self, value=None):
    self.values.append(int(value))

  def countDimension(self):
    self.dimension = len(self.values)
    
  def displayData(self):
    print("ID : ", self.id, "\nTimestamp start : ",self.timestamp_in, "\nTimestamp end : ",self.timestamp_out,"\nValues : ", self.values, "\n")

  def displayDataCount():
    print("Total data : ", Product.data_count)

  def displayDimensionCount(self):
    print("Total dimensi : ", self.dimension)

class Product(Data):
  def __init__(self, id, timestamp_in, timestamp_out):
    Data.__init__(self, id, timestamp_in, timestamp_out)

class Customer(Data):
  dsl_count = 0

  def __init__(self, id, timestamp_in, timestamp_out):
    Data.__init__(self, id, timestamp_in, timestamp_out)    
    self.dsl_results = []

  def addDslResult(self, dsl_result):
    self.dsl_results.append(dsl_result)
    self.dsl_count += 1

  def countProbability(self):
    return 1/dsl_count

class EventQueue:
  def __init__(self):
    self.events = []

  def isEmpty(self):
    return self.events == []

  def enqueue(self, timestamp, owner, owner_id, action):
    self.event = []
    self.event.append(int(timestamp))
    self.event.append(owner) 
    self.event.append(int(owner_id)) 
    self.event.append(action)
    self.events.append(self.event)

  def dequeue(self):
    return self.events.pop()

  def getKey(self, item):
    return item[0]

  def sortQueue(self):
    self.events = sorted(self.events, key=self.getKey, reverse=True)
  
  def displayQueue(self):
    return '{}'.format(self.events)
  
class PandoraBox:
  def __init__(self):
    self.box = []

  def addScore(self, product_id, event_id, score):
    self.box[product_id][event_id] = score

class Domination:
  def __init__(self):
    self.box = []

  def addProduct(self, product_id, customer_id, dom_product_id):
    self.box[product_id][customer_id].append(dom_product_id) 

class CustomerThread(threading.Thread):
  def __init__(self, thread_name): 
    self._stopevent = threading.Event()
    self._sleepperiod = 1.0
    threading.Thread.__init__(self, name = thread_name) 

  def run(self):
    print("%s starts" % (self.getName(),))
    count = 0
    while not self._stopevent.isSet():
      count += 1
      processThread()
      self._stopevent.wait(self._sleepperiod)
    print ("%s ends" % (self.getName(),))

  def kill(self, thread_name):
    self._stopevent.set()
    threading.Thread.join(self, name = thread_name)

def processThread():
  while True:
    print('thread running')

def inputCsv(data_name, file, delimiter, event_queue):
  list = []
  row_count = 0

  with open(file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
    for row in csv_reader:
      col_count = len(csv_reader.fieldnames)
      
      if data_name == "product":
        object = Product(row[csv_reader.fieldnames[0]], row[csv_reader.fieldnames[1]], row[csv_reader.fieldnames[2]])
        owner = "p"
      elif data_name == "customer":
        object = Customer(row[csv_reader.fieldnames[0]], row[csv_reader.fieldnames[1]], row[csv_reader.fieldnames[2]])
        owner = "c"

      list.append(object)
      
      for j in range(3,col_count):
        list[row_count].addValue(row[csv_reader.fieldnames[j]])
      
      row_count += 1

      # menambah event ke queue
      event_queue.enqueue(row[csv_reader.fieldnames[1]], owner, row[csv_reader.fieldnames[0]], "in")
      event_queue.enqueue(row[csv_reader.fieldnames[2]], owner, row[csv_reader.fieldnames[0]], "out")
  
  return list

if __name__ == '__main__':
  event_queue = EventQueue()
  product_list = []
  customer_list = []
  threads = []
  thread_id = 1

  # Masukkan data 
  files = int(input("Enter number of files: "))
  for i in range(files):
    data_name = input("Enter the data name ({}) : ".format(i+1))
    file = input("Input the file : ")
    delimiter = input("Delimiter type : ")
    if data_name == "product":
      product_list = inputCsv(data_name, file, delimiter, event_queue)
    elif data_name == "customer": 
      customer_list = inputCsv(data_name, file, delimiter, event_queue)    

  # print data
  print("Product \n")
  for product in product_list:
    product.displayData()

  print("Customer \n")
  for customer in customer_list:
    customer.displayData()

  # mengurutkan event
  event_queue.sortQueue()
  print(event_queue.displayQueue())

  # mengeluarkan event
  while not event_queue.isEmpty():
    event = event_queue.dequeue()
    print(event)
    
    if event[1] == "c" and event[3] == "in":
      print("Make a thread\n")
      thread = CustomerThread(event[1]+event[2])
      thread.start()
      time.sleep(2)
      thread.kill()
      threads.append(thread)
      thread_id += 1
    
    elif event[1] == "c" and event[3] == "out":
      print("Kill a thread\n")
      

    elif event[1] == "p" and event[3] == "in":
      print("Product in\n")

    elif event[1] == "p" and event[3] == "out":
      print("Product out\n")
