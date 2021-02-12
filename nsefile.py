
from nsetools import nse

import time

import threading

def printit(key):
    print(key)

fno = nse.Nse()

lis=fno.get_fno_lot_sizes(as_json=False);

lis = dict(lis);
keys= list(lis.keys())

print(keys[0])

# print(fno.get_quote(code=keys[2]))

for key in keys[4:]:
    print(key.ljust(20) , str(lis[key]).rjust(20),str(fno.get_quote(key)['closePrice']).rjust(20),'{0:,}'.format(lis[key]*fno.get_quote(key)['closePrice']),sep='\t\t\t')
    # time.sleep(1)
    
#     
