import csv
from app.src.kmpp.pandora_box import PandoraBox

def kmpp_solution(file, k_product, time_start, time_end):
    pandora_box = PandoraBox()
    market_contr = {}
    output = []

    k_product = int(k_product)
    time_start = int(time_start)
    time_end = int(time_end)
     
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        total_prod = 0
        for row in csv_reader:
            prod_score = []
            for col in row:
                prod_score.append(float(col))
            pandora_box.insert_score(prod_score) 
            total_prod += 1

    # hitung kontribusi pasar total selama interval waktu
    # asumsi id product integer yang berurutan
    for i in range(1, total_prod):
        market_contr[i] = pandora_box.get_score(i, time_start, time_end)
    print('Market Contribution')
    for key in market_contr:
        print('{} : {}'.format(key, market_contr[key]))

    # sort yang paling besar
    sorted_prod = sorted(market_contr, key=lambda x: (market_contr[x]), reverse=True)

    # keluarkan output k teratas
    for i in range(0, k_product):
        product = {}
        product['id'] = sorted_prod[i]
        product['market_contr']= market_contr[sorted_prod[i]]
        output.append(product)

    return output
