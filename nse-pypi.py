from nse import Nse
import time
from nsetools import nse


db = Nse()
fno = nse.Nse()

lis=fno.get_fno_lot_sizes(as_json=False);

fno_lot = dict(lis)
keys= list(fno_lot.keys())
print(keys)
for key in keys[10:]:
    try:
        price=db.live(key)['lastPrice']
        if price*lis[key] > 200000 and price*lis[key]  < 500000:
            print(key.ljust(20),str(lis[key]).ljust(20),str(price).ljust(20),"{:,}".format(price*lis[key]))
    except:
        pass    
        # time.sleep(1)
# print(data)
