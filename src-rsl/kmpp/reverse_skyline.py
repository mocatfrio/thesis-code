import sys
from .custom_logger import logger

"""
Reverse Skyline Computation Handling
    1. menentukan orthant
    2. menghitung midpoint antar produk
    3. menentukan midpoint skyline setiap orthant
    4. mencari pelanggan yang tidak didominasi oleh midskyline
"""

class ReverseSkyline:
    def __init__(self, id, product, customer, max_val):
        self.my_id = id
        self.my_value = product[id]['value']
        self.product = product
        self.customer = customer
        self.dim = len(max_val)
        self.max_val = max_val

    def define_orthant(self):
        self.orthant = {}
        for i in range(2**self.dim): 
            id = binary(i, self.dim)
            self.orthant[id] = {}
    
    def get_orthant_area(self, product_val):
        res = []
        for i in range(self.dim):
            if product_val[i] <= self.my_value[i]:
                res.append('0')
            else:
                res.append('1')
        res = ''.join(res)
        return res

    def print_orthant(self):
        logger.info('{}'.format(self.orthant))

    def calc_midpoint(self, val1, val2):
        res = []
        for i in range(self.dim):
            res.append((val1[i] + val2[i])/2)
        logger.info('Midpoint = {}'.format(res))
        return res

    def find_midpoint_skyline(self):
        for id in self.product:
            if id == self.my_id:
                continue
            midpoint = self.calc_midpoint(self.my_value, self.product[id]['value'])
            area = self.get_orthant_area(self.product[id]['value'])
            if not self.orthant[area]:
                self.orthant[area][id] = midpoint
            else:
                self.orthant[area] = self.is_skyline(self.orthant[area], midpoint, id)
            logger.info('Midpoint skyline = {}'.format(self.orthant[area]))
 
    def find_reverse_skyline(self):
        pass

    def is_skyline(self, current, candidate, candidate_id):
        res = {}
        for i in list(current.keys()):
            if self.is_dominating(candidate, current[i]):
                res[candidate_id] = candidate                
            else:
                res[i] = current[i]
                if not self.is_dominating(current[i], candidate):
                    res[candidate_id] = candidate
        return res
    
    def is_dominating(self, subject, target):
        dominating = 0
        dominated = 0
        for i in range(0, self.dim):
            subj_diff = abs(self.my_value[i] - subject[i])
            target_diff = abs(self.my_value[i] - target[i])
            if subj_diff == target_diff:
                continue
            elif subj_diff < target_diff:
                dominating += 1
            else:
                dominated += 1
        if dominated == 0 and dominating >= 1:
            return True
        else:
            return False
    
def binary(num, length):
    return format(num, '#0{}b'.format(length + 2))[2:]