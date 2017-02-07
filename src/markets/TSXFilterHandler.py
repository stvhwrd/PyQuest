'''TSXFilterHandler

@summary: Fetches all TSX listings and their data. Leverages numpy arrays
   to easily filter results


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

import questrade.api.market as api_market
from sqlite import tsx_listings
import numpy as np


class TSXFilterHandler(object):

    market_data = {}
    quote_data = {}
    
    __volume_percentile_threshold = 90
    __largecap_percentile_threshold = 90
    __opengapping_percentile_threshold = 90
    __daymovers_percentile_threshold = 90

    def __init__(self):
        pass
    
    def fetch_market_data(self):
        ids = tsx_listings.get_symbol_ids()
        r = api_market.symbolIds(ids);
        if 'symbols' in r:
            symbols = r.get('symbols')
            for s in symbols:
                for k, v in s.items():
                    if k in self.market_data:
                        self.market_data[k].append(v)
                    else:
                        self.market_data.update({k:[v]})
    
    def fetch_quote_data(self):
        ids = tsx_listings.get_symbol_ids()
        r = api_market.markets_quotes(ids)
        if 'quotes' in r:
            quotes = r.get('quotes')
            for q in quotes:
                for k, v in q.items():
                    if k in self.quote_data:
                        self.quote_data[k].append(v)
                    else:
                        self.quote_data.update({k:[v]})
                    
    def get_market_data(self, key):
        a = self.market_data[key]
        a = [i if i is not None else 0 for i in a] # replace all None elements with 0
        return np.array(a)
    
    def get_quote_data(self, key):
        a = self.quote_data[key]
        a = [i if i is not None else 0 for i in a] # replace all None elements with 0
        return np.array(a)
        
    def get_averageVol20Days_stocks(self):
        s = self.get_market_data('symbol')
        a = self.get_market_data('averageVol20Days')
        
        percentile_threshold = np.percentile(a, self.__volume_percentile_threshold)
        
        s = s[np.where(a >= percentile_threshold)]
        return s
    
    def get_interdayvolume_stocks(self):
        s = self.get_market_data('symbol')
        a = self.get_quote_data('volume')
        
        percentile_threshold = np.percentile(a, self.__volume_percentile_threshold)
        
        s = s[np.where(a >= percentile_threshold)]
        return s
    
    def get_largecap_stocks(self):
        s = self.get_market_data('symbol')
        a = self.get_market_data('marketCap')
        
        percentile_threshold = np.percentile(a, self.__largecap_percentile_threshold)
        
        s = s[np.where(a >= percentile_threshold)]
        return s
    
    def get_minprice_stocks(self, min_price):
        s = self.get_market_data('symbol')
        p = self.get_market_data('prevDayClosePrice')
        
        s = s[np.where(p >= min_price)]
        return s
    
    def get_industrysector_stocks(self, industrysector):
        s = self.get_market_data('symbol')
        a = self.get_market_data('industrySector')
        
        s = s[np.where(a == industrysector)]
        return s
    
    def get_industrygroup_stocks(self, industrygroup):
        s = self.get_market_data('symbol')
        a = self.get_market_data('industryGroup')
        
        s = s[np.where(a == industrygroup)]
        return s
    
    def get_opengapping_stocks(self):
        s = self.get_market_data('symbol')
        p = self.get_market_data('prevDayClosePrice')
        o = self.get_quote_data('openPrice')
        
        x = np.nonzero(o)
        s = s[x]
        p = p[x]
        o = o[x]
        
        diffs = np.abs(o - p)
        
        x = np.nonzero(diffs)
        s = s[x]
        p = p[x]
        diffs = diffs[x]
        
        diffs = np.divide(diffs, p)
                
        percentile_threshold = np.percentile(diffs, self.__opengapping_percentile_threshold)
        
        s = s[np.where(diffs >= percentile_threshold)]
        return s
    
    def get_daymovers_stocks(self):
        s = self.get_market_data('symbol')
        o = self.get_quote_data('openPrice')
        l = self.get_quote_data('lastTradePrice')
        
        x = np.nonzero(o)
        s = s[x]
        o = o[x]
        l = l[x]
        
        diffs = np.abs(l - o)
        
        x = np.nonzero(diffs)
        s = s[x]
        o = o[x]
        diffs = diffs[x]
        
        diffs = np.divide(diffs, o)
                
        percentile_threshold = np.percentile(diffs, self.__daymovers_percentile_threshold)
        
        s = s[np.where(diffs >= percentile_threshold)]
        return s
    
    @staticmethod
    def intersection(*args):
        if args is None or len(args) == 0:
            return np.array([])
        r = args[0]
        if len(args) > 1:
            l = args[1:]
            for a in l:
                r = np.intersect1d(r, a)
        return r



if __name__ == '__main__':
    t = TSXFilterHandler()
    t.fetch_market_data()
    t.fetch_quote_data()
    
    a = t.get_largecap_stocks()
    b = t.get_minprice_stocks(10)
    c = t.get_averageVol20Days_stocks()
    d = t.get_interdayvolume_stocks()
    e = t.get_opengapping_stocks()
    f = t.get_daymovers_stocks()
    
    z = TSXFilterHandler.intersection(b,d,f)
    z = np.sort(z)
    print z
   
    
    