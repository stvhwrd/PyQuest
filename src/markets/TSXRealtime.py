'''TSXRealtime

@summary: Provided TSX Realtime data


@copyright: 2017
@author: Peter Cinat
@license: Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from threading import Thread
from datetime import datetime
from markets.TSXFilterHandler import TSXFilterHandler
import numpy as np
import time


def tsx_realtime(sleep_time):
    tsx_data = TSXFilterHandler()
    
    while True:
        tsx_data.fetch_market_data()
        tsx_data.fetch_quote_data()
        
        #a = tsx_data.get_largecap_stocks()
        b = tsx_data.get_minprice_stocks(10)
        #c = tsx_data.get_averageVol20Days_stocks()
        d = tsx_data.get_interdayvolume_stocks()
        e = tsx_data.get_opengapping_stocks()
        f = tsx_data.get_daymovers_stocks()
        
        b_n_d = TSXFilterHandler.intersection(b,e)
        
        print "Stocks with an opening gap:"
        z = TSXFilterHandler.intersection(b,e)
        z = np.sort(z)
        print z
        
        print "Stocks with big daily moves:"
        z = TSXFilterHandler.intersection(b_n_d,f)
        z = np.sort(z)
        print z
        
        time.sleep(sleep_time)


if __name__ == '__main__':
    print "=================================================="
    print "TSX Realtime market data"
    t1 = datetime.now()
    print "Start time: %s" % t1.isoformat()
    
    th1 = Thread(target=tsx_realtime, args=(60,))
    th1.daemon = True
    th1.start()
    
    th1.join()
    
    t2 = datetime.now()
    tdelta = t2 - t1
    
    print "End time: %s" % t2.isoformat()
    print "Total time: %s" % str(tdelta)
    