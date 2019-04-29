import csv
from app.src.kmpp.pandora_box import PandoraBox

def kmpp(file, k_product, time_start, time_end):
    pandora_box = PandoraBox()
    market_contr = {}
    output = {}
     
    # file = '../static/csv/pandora_box.csv'
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        total_prod = 0
        for row in csv_reader:
            prod_score = []
            for col in row:
                prod_score.append(float(col))
            pandora_box.insert_score(prod_score) 
            total_prod += 1
    pandora_box.print_box()

    # k_product = int(input('Masukkan jumlah produk : '))
    print('Jumlah produk: {}'.format(k_product))
    # time_start, time_end = input('Masukkan waktu awal dan akhir (dipisahkan oleh spasi): ').split()
    print('Interval waktu: {} - {}'.format(time_start, time_end))

    # hitung kontribusi pasar total selama interval waktu
    # asumsi id product integer yang berurutan
    for i in range(0, total_prod):
        market_contr[i] = pandora_box.get_score(i, int(time_start), int(time_end))
    print('Market Contribution')
    for key in market_contr:
        print('{} : {}'.format(key, market_contr[key]))

    # sort yang paling besar
    sorted_prod = sorted(market_contr, key=lambda x: (market_contr[x]), reverse=True)
    print(sorted_prod)

    # keluarkan output k teratas
    for i in range(0, k_product):
        output[sorted_prod[i]] = market_contr[sorted_prod[i]]

    print(output)

    return output
