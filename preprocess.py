# INDEX CREATION
# input   : products.csv, customers.csv
# output  : gridproducts.txt, gridcustomers.txt, gridinfo.txt
#
# 3. tentukan nilai max masing2 dimensi
# 4. tentukan nilai max dari semua dimensi
# 5. tentukan grid size (awalnya static aja dulu 3x3) 
# 6. hitung vector position dari masing2 ob data 
# 
# output: file txt
# ob masing-masing position di simpen ke array sementara
# setelah semua data udh, bikin file grid info
#

import csv

class DataObject:
  data_count = 0
  dimension_count = 0

  def __init__(self, id=None, timestamp_start=None, timestamp_end=None, vector_position=None):
    self.id = id
    self.vector_position = vector_position
    self.timestamp_start = timestamp_start
    self.timestamp_end = timestamp_end
    self.values = []
    DataObject.data_count += 1

  def addValue(self, value=None):
    self.values.append(value)
    self.dimension_count += 1

  def findMax(self):
    max_value = []
    
  
  def displayData(self):
    print("ID : ", self.id, "\nTimestamp start : ",self.timestamp_start, "\nTimestamp end : ",self.timestamp_end,"\nVector Position : ", self.vector_position, "\nValues : ", self.values)

  def displayDataCount():
    print("Total data : ", DataObject.data_count)

  def displayDimensionCount(self):
    print("Total dimensi : ", self.dimension_count)

  


total_file = int(input("Masukkan jumlah data : "))

for i in range(total_file):
  print("===================================================================")
  file = input("Masukkan file ({}) : ".format(i+1))
  delimiter = input("Jenis delimiter : ")
  print("===================================================================")
  data_list = []
  row_count = 0 

  with open(file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=delimiter)

    for row in csv_reader:
      col_count = len(csv_reader.fieldnames)
      data_list.append(DataObject(row[csv_reader.fieldnames[0]], row[csv_reader.fieldnames[1]], row[csv_reader.fieldnames[2]]))
      for j in range(3,col_count):
        data_list[row_count].addValue(row[csv_reader.fieldnames[j]])
      
      data_list[row_count].displayData()
      data_list[row_count].displayDimensionCount()
      print("\n")
      row_count += 1

    DataObject.displayDataCount()





  


