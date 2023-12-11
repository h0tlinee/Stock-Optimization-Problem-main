
from Stock import *
import random

def rand_type():
    i = random.randint(1, 3)
    if i == 1:
        return "1"
    elif i == 2:
        return "2"
    else:
        return "3"
    
def rand_id():
    r = random.randint(1, 14)
    if r < 10:
        return '000'+str(r)
    else:
        return '00'+str(r)
    
def rand_quant(a, b):
    return random.randint(a, b)


            

