import csv, sys, threading, os
import cProfile
import logging
import numpy as np
from kmpp.pandora_box import PandoraBox
from kmpp.event_queue import EventQueue
from kmpp.reverse_skyline import ReverseSkyline
from kmpp.dynamic_skyline import DynamicSkyline

"""
Data Handling
"""
def input_csv(dataset, event_queue):
  data = {}
  for i in range(len(dataset)):
    logging.info('Input data {}'.format(dataset[i]))
    if i == 0:
      data['product'] = data_indexing(i, dataset[i], event_queue)
    else:
      data['customer'] = data_indexing(i, dataset[i], event_queue)
  return data

def data_indexing(data_id, data_file, event_queue):
  data = {}
  with open(data_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
      col_cnt = len(csv_reader.fieldnames)
      id = int(row[csv_reader.fieldnames[0]])
      data[id] = {}
      data[id]['ts_in'] = int(row[csv_reader.fieldnames[2]])
      data[id]['ts_out'] = int(row[csv_reader.fieldnames[3]])
      data[id]['value'] = []
      for i in range(4, col_cnt):
        data[id]['value'].append(int(row[csv_reader.fieldnames[i]]))
      for i in range(0, 2):
        event_queue.enqueue(data[id]['ts_in'] if i == 0 else data[id]['ts_out'], data_id, id, i)
  logging.info('Data ({}) succesfully inputed'.format(data_file))
  return data

def print_data(data):
  for key, values in data.items():
    logging.info('{}'.format(key))
    for k, v in values.items():
      logging.info('{} : {}'.format(k, v))

def get_max_value(data):
  all_val = []
  for val1 in data.values():
    for val2 in val1.values():
      all_val.append(val2['value'])
  return np.max(all_val, axis=0)

def main(dataset):
  data = {}
  event_queue = EventQueue()

  data = input_csv(dataset, event_queue)
  print_data(data)
  max_val = get_max_value(data)

  event_queue.sort_queue()
  pandora_box = PandoraBox(len(data['product']) + 1, event_queue.get_max_timestamp() + 1)

  data['product']['active'] = []
  data['customer']['active'] = []

  rsl = ReverseSkyline(data['product'], data['customer'], max_val)
  dsl = DynamicSkyline(data['product'], data['customer'], max_val, pandora_box)

  # Event
  while not event_queue.is_empty():
    logging.info('UPDATE CUST')
    for cust in data['customer']:
      try:
        pass
        logging.info('C-{} : {}'.format(cust, data['customer'][cust]['dsl']))
      except:
        pass
    logging.info('UPDATE PBOX')
    pandora_box.print_box()

    event = event_queue.dequeue()
    if event[1] == 0:
      if event[3] == 0:
        """
        Product in:
          1. Tambah ke produk aktif
          2. Hitung RSL
          3. Setiap RSL: Hitung DSL
          4. Update Pandora Box
        """
        logging.info('=================================================================')
        logging.info('[P-{} IN]'.format(event[2]))

        data['product']['active'].append(event[2])
        logging.info('[P-{} IN] Masuk ke produk aktif: {}'.format(event[2], data['product']['active']))  
        
        rsl_result = rsl.start_computation(event[2])
        
        for customer_id in rsl_result:
          dsl.start_computation(customer_id, event[0], event[3], event[2])
        
        for customer_id in data['customer']['active']:
          dsl.start_computation(customer_id, event[0], 2)

        # threads = []
        # for customer_id in rsl_result:
        #   t = threading.Thread(target=dsl.start_computation, args=(customer_id, event[0], event[3], event[2]))
        #   threads.append(t)
        # for t in threads:
        #   t.start()
        # for t in threads:
        #   t.join()
        logging.info('=================================================================')
      
      elif event[3] == 1:
        """
        Product out:
          1. Update Pandora Box
          2. Hitung RSL
          3. Setiap RSL: Hitung DSL
          4. Hapus dari produk aktif
          5. Setiap RSL: Hitung Init DSL
          6. Bandingkan jika hasil DSL tidak sama maka masukkan hasil yg baru
        """
        logging.info('=================================================================')
        logging.info('[P-{} OUT]'.format(event[2]))

        for customer_id in data['customer']['active']:
          dsl.start_computation(customer_id, event[0], 2)

        rsl_result = rsl.start_computation(event[2])
        
        for customer_id in rsl_result:
          dsl.start_computation(customer_id, event[0], event[3], event[2])

        # threads = []
        # for customer_id in data['customer']['active']:
        #   t = threading.Thread(target=dsl.start_computation, args=(customer_id, event[0], event[3], event[2]))
        #   threads.append(t)
        # for t in threads:
        #   t.start()
        # for t in threads:
        #   t.join()
        
        data['product']['active'].remove(event[2])
        logging.info('[P-{} OUT] Hapus dari produk aktif: {}'.format(event[2], data['product']['active']))

        for customer_id in rsl_result:
          dsl_res = dsl.start_computation(customer_id, event[0], 3)
          try:
            logging.info('new_dsl = {}'.format(dsl_res))
            logging.info('current_dsl = {}'.format(data['customer'][customer_id]['dsl']))
            if sorted(dsl_res) != sorted(data['customer'][customer_id]['dsl']):
              data['customer'][customer_id]['dsl'] = dsl_res
          except:
            data['customer'][customer_id]['dsl'] = dsl_res
          logging.info('dsl = {}'.format(data['customer'][customer_id]['dsl']))        
        logging.info('=================================================================')
    
    elif event[1] == 1:
      if event[3] == 0:
        """
        Customer in:
          1. Tambah ke pelanggan aktif
          2. Menghitung initial dsl
        """
        logging.info('=================================================================')
        logging.info('[C-{} IN]'.format(event[2]))
        
        data['customer']['active'].append(event[2])
        logging.info('[C-{} IN] Masukkan ke customer aktif: {}'.format(event[2], data['customer']['active']))
        
        dsl.start_computation(event[2], event[0])
        dsl.start_computation(event[2], event[0], 2)
        logging.info('=================================================================')

      elif event[3] == 1:
        """
        Customer out:
          1. Update pandora box
          2. Hapus dari pelanggan aktif
        """
        logging.info('=================================================================')
        logging.info('[C-{} OUT]'.format(event[2]))
        dsl.start_computation(event[2], event[0], 2)
        
        data['customer']['active'].remove(event[2])
        logging.info('[C-{} OUT] Hapus dari produk aktif: {}'.format(event[2], data['customer']['active']))
        logging.info('=================================================================')

  pandora_box.print_box()
  pandora_box.export_csv()

  logging.info('Exiting the main program') 

if __name__ == "__main__":
  if not os.path.exists('log'):
    os.mkdir('log')
  logging.basicConfig(
      filename='log/app.log', 
      filemode='w', 
      format='[%(levelname).1s] %(threadName)12s: %(message)s',
      level=logging.INFO
    )
  dataset = ['product.csv', 'customer.csv']

  pr = cProfile.Profile()
  pr.enable()
  main(dataset)
  pr.disable()
  pr.print_stats()