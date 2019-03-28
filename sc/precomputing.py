import logging

from kmpp.data import *
from kmpp.event_queue import *
from kmpp.pandora_box import *
from kmpp.customer_thread import *

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

def 

if __name__ == '__main__':
  # declare variable
  product_list, customer_list, threads, product_active = [], [], [], []
  event_queue = EventQueue()
  declare_threading_event()
  
  # input data 
  files = int(input("Enter number of files: "))
  for i in range(files):
    data_name = input("Enter the data name ({}) : ".format(i+1))
    file = input("Input the file : ")
    delimiter = input("Delimiter type : ")
    if data_name == "product":
      product_list = input_csv(data_name, file, delimiter, event_queue)
    elif data_name == "customer": 
      customer_list = input_csv(data_name, file, delimiter, event_queue)    

  # DEBUG
  # print data
  print("Product \n")
  for product in product_list:
    print(product.display_data())
  print("Customer \n")
  for customer in customer_list:
    print(customer.display_data())

  # mengurutkan event
  event_queue.sort_queue()
  # DEBUG
  print(event_queue.display_queue())

  # mengeluarkan event
  while not event_queue.is_empty():
    event = event_queue.dequeue()
    # DEBUG
    print('\nEVENT {}'.format(event))
    
    if event[1] == 0 and event[3] == 1:
      # DEBUG
      print("\nMake a thread")

      if product_active:
        thread = CustomerThread(event[2], customer_list, product_active, product_list)
        thread.start()
        threads.append(thread)
      else:
        thread = CustomerThread(event[2])
        thread.start()
        threads.append(thread)

    elif event[1] == 0 and event[3] == 0:
      # DEBUG  
      print("\nKill a thread")

      index = find_thread(threads, lambda x: x.thread_id == event[2])
      threads[index].kill_thread()
      threads[index].join()

    elif event[1] == 1 and event[3] == 1:
      print("\nProduct in")
      product_active.append(event[2])
      print('produk aktif: {} \n'.format(product_active))

    elif event[1] == 1 and event[3] == 0:
      print("\nProduct out")
      product_active.remove(event[2])
      print('\nproduk aktif: {} \n'.format(product_active))

  # for thread in threads:
  #   thread.join()

  print("\nExiting the main program")  