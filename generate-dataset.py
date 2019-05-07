import random
import sys
import csv

DATASET_PATH = "dataset/"

def data_random(arg=None):
    rand_a = random.randint(1,200)
    rand_b = rand_a + random.randint(1,100)
    if arg is not None:
        rand_b = arg + random.randint(90,100)
        rand = random.randint(arg, rand_b)
    else:
        rand = random.randint(rand_a, rand_b)
    return rand

try:
    num_of_rows = int(sys.argv[1])
except IndexError:
    num_of_rows = 100

try:
    num_of_dim = int(sys.argv[2])
except IndexError:
    num_of_dim = 2

try:
    data_name = sys.argv[3]
except:
    data_name = 'item'

res = []

title_row = ["id", "label", "ts_in", "ts_out"]
for i in range(num_of_dim):
    title_row.append("dim_"+str(i))
res.append(title_row)

for i in range(num_of_rows):
    data_row = [i+1, data_name + "-" + str(i+1)]
    data_row.append(data_random())
    data_row.append(data_random(data_row[2]))
    for j in range(num_of_dim):
        data_row.append(data_random())
    res.append(data_row)

csvfile = DATASET_PATH + "dataset_" + data_name + "_" + str(num_of_rows) + "_" + str(num_of_dim) + ".csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(res)