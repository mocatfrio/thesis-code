import random, sys, os, csv, math

DATASET_PATH = os.path.join(os.getcwd(), '../deploy/dataset/')
MAX_VALUE = 200
DISTANCE = 5

def data_random(arg=None):
    rand_a = random.randint(0, MAX_VALUE)
    rand_b = rand_a + random.randint(0, MAX_VALUE/2)
    if arg is not None:
        rand_b = arg + random.randint(MAX_VALUE/2 - math.sqrt(MAX_VALUE/2), MAX_VALUE/2)
        rand = random.randint(arg, rand_b)
    else:
        rand = random.randint(rand_a, rand_b)
    return rand

if __name__ == "__main__":
    try:
        dataset_type = sys.argv[1]
    except:
        dataset_type = 'i'

    try:
        num_of_rows = int(sys.argv[2])
    except IndexError:
        num_of_rows = 100

    try:
        num_of_dim = int(sys.argv[3])
    except IndexError:
        num_of_dim = 2

    try:
        data_name = sys.argv[4]
    except:
        data_name = 'item'

    res = []
    title_row = ["id", "label", "ts_in", "ts_out"]
    # Masukkan nama kolom
    for i in range(num_of_dim):
        title_row.append("dim_"+str(i))
    res.append(title_row)
    # Random data
    for i in range(num_of_rows):
        data_row = [i+1, data_name + "-" + str(i+1)]
        data_row.append(data_random())
        data_row.append(data_random(data_row[2]))
        if dataset_type == 'i':
            for j in range(num_of_dim):
                data_row.append(data_random())
        elif dataset_type == 'ac':
            # generate anti-correlated
            rand = data_random()
            select_dim = random.randint(0, num_of_dim - 1)
            for j in range(num_of_dim):
                if j == select_dim:
                    data_row.append(rand)
                else:
                    val_of_other_dim = MAX_VALUE - rand + random.randint(-DISTANCE,DISTANCE)
                    if val_of_other_dim < 0:
                        data_row.append(0)
                    elif val_of_other_dim > MAX_VALUE:
                        data_row.append(MAX_VALUE)
                    else:
                        data_row.append(val_of_other_dim)
        res.append(data_row)

    if dataset_type == 'i':
        new_path = DATASET_PATH + "ind/"
    elif dataset_type == 'ac':
        new_path = DATASET_PATH + "ant/"
        
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    csvfile = new_path + data_name + '_' + dataset_type + '_' + str(num_of_rows) + "_" + str(num_of_dim) + ".csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(res)

