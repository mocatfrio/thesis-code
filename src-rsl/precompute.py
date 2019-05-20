import csv, sys, threading, logging, os
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
        logging.info('C-{} : {}'.format(cust, data['customer'][cust]['dsl']))
      except:
        logging.info('C-{} : blum ada DSL'.format(cust))

    event = event_queue.dequeue()
    if event[1] == 0:
      if event[3] == 0:
        """
        Product in:
        1. Menambah produk aktif
        2. Menghitung RSL(p)
        3. Bikin thread untuk menghitung DSL(RSL(p))
        """
        # threads = []
        data['product']['active'].append(event[2])
        logging.info('[P-{} in] Masuk ke produk aktif: {}'.format(event[2], data['product']['active']))  
        rsl_result = rsl.start_computation(event[2])
        logging.info('[P-{} in] - Start threading'.format(event[2]))
        for customer_id in rsl_result:
          dsl.start_computation(customer_id, event[0], event[3], event[2])

        # for customer_id in rsl_result:
        #   t = threading.Thread(target=dsl.start_computation, args=(customer_id, event[0], event[3], event[2]))
        #   threads.append(t)
        # for t in threads:
        #   t.start()
        # for t in threads:
        #   t.join()
        logging.info('[P-{} in] - Komputasi selesai'.format(event[2]))
      
      elif event[3] == 1:
        """
        Product out:
        1. Menghapus dari produk aktif
        """
        # threads = []
        rsl_result = rsl.start_computation(event[2])
        logging.info('[P-{} out] - Start threading'.format(event[2]))
        for customer_id in rsl_result:
          dsl.start_computation(customer_id, event[0], event[3], event[2])

        # for customer_id in data['customer']['active']:
        #   t = threading.Thread(target=dsl.start_computation, args=(customer_id, event[0], event[3], event[2]))
        #   threads.append(t)
        # for t in threads:
        #   t.start()
        # for t in threads:
        #   t.join()
        logging.info('[P-{} out] - Komputasi selesai'.format(event[2]))
        data['product']['active'].remove(event[2])
        logging.info('[P-{} out] Hapus dari produk aktif: {}'.format(event[2], data['product']['active']))
    elif event[1] == 1:
      if event[3] == 0:
        """
        Customer in:
        1. Menambah pelanggan aktif
        2. Menghitung initial dsl
        """
        logging.info('[C-{} in] Make thread'.format(event[2]))
        data['customer']['active'].append(event[2])
        logging.info('[C-{} in] Masukkan ke customer aktif: {}'.format(event[2], data['customer']['active']))
        dsl.start_computation(event[2], event[0])
      elif event[3] == 1:
        """
        Customer out
        """
        logging.info('[C-{} out] Kill thread'.format(event[2]))
        dsl.start_computation(event[2], event[0], 2)
        data['customer']['active'].remove(event[2])
        logging.info('[C-{} out] Hapus dari produk aktif: {}'.format(event[2], data['customer']['active']))

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
  main(dataset)
