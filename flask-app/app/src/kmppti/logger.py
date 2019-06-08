"""
Logger Handling
"""

import os, datetime, time, os, psutil, csv
from app import app

class Logger:
  data_info = []

  def __init__(self, algo, process):
    self.time_start = None
    self.time_end = None
    self.ts_start = None
    self.ts_end = None
    self.runtime = None
    self.mem_usage = None
    self.algo = algo
    self.process = process
    self.query_info = []
  
  def set_time(self, time_type):
    time_now = datetime.datetime.now()
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d__%H:%M:%S')
    if time_type == 0:
      self.time_start = time_now
      self.ts_start = ts
    elif time_type == 1:
      self.time_end = time_now
      self.ts_end = ts
    else:
      print('Anda hanya dapat memasukkan angka 0 atau 1')

  def set_runtime(self):
    time = self.time_end - self.time_start
    self.runtime = time
    print('Program finished with runtime {}'.format(self.runtime))

  def set_mem_usage(self):
    process = psutil.Process(os.getpid())
    mem = float(process.memory_info().rss)/1000000.0
    self.mem_usage = mem
    print('Memory usage: {}'.format(self.mem_usage))

  def set_data_info(self, info):
    Logger.data_info = info

  def set_query_info(self, k_product, time_start, time_end):
    if self.query_info:
      self.query_info = []

    self.query_info.append(k_product)
    self.query_info.append(time_start)
    self.query_info.append(time_end)

  def export_log(self):
    res_title = ['process', 'ts_start', 'ts_end', 'algorithm', 'data_type', 'num_of_rows', 'num_of_dimensions', 'query_info', 'run_time', 'mem_usage']
    res, res_data = [], []
    res_data.append(self.process)
    res_data.append(self.ts_start)
    res_data.append(self.ts_end)
    res_data.append(self.algo)
    try:
      res_data.append(self.data_info[1])
      res_data.append(self.data_info[2])
      res_data.append(self.data_info[3].split('.')[0])
    except:
      res_data.append('unknown')
      res_data.append('unknown')
      res_data.append('unknown')
    try:
      info = 'k : ' + str(self.query_info[0]) + ' | time intvl : ' + str(self.query_info[1]) + '-' + str(self.query_info[2])
    except IndexError:
      info = '-'
    res_data.append(info)
    res_data.append(self.runtime)
    res_data.append(self.mem_usage)
    res.append(res_data)
    
    if not os.path.exists(app.config['LOG_DIR']):
      os.mkdir(app.config['LOG_DIR'])
    log_path = app.config['LOG_DIR'] + '/log.csv'
    print('Saved to {}'.format(log_path))
    if not os.path.exists(log_path):
      with open(log_path, 'a') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(res_title)
    with open(log_path, 'a') as output:
      writer = csv.writer(output, lineterminator='\n')
      writer.writerows(res)

  