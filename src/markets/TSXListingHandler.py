'''TSXListingHandler

@summary: Fetches all TSX listings and stores them in a local SQLite database


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

import os
import json
import requests
from configparser import SafeConfigParser
from sqlite import tsx_listings
from questrade.api import utils
from threading import Thread, Event
from datetime import datetime


class TSXListingHandler(object):

    base_url = ""
    search_options = []

    def __init__(self):
        config = SafeConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tsx_config.cfg'))
        
        self.base_url = config.get('TSX', 'base_url')
        self.search_options = json.loads(config.get('TSX', 'search_options'))
    
    def fetchListings(self, s):
        headers = ""
        params = ""
        uri = self.base_url + s
        
        try:
            r = requests.get(uri, headers=headers, params=params)
            response = r.json()
            
            if 'results' in response:
                results = response.get('results')
                
                for result in results:
                    if 'instruments' in result:
                        instruments = result.get('instruments')
                        if instruments is not None:
                            for i in instruments:
                                symbol = str(i.get('symbol', ''))
                                symbol = self.__convert_symbol_for_questrade__(symbol)
                                name = str(i.get('name', ''))
                                id_ = utils.lookup_symbol_id(symbol)
                                if id_ != -1:
                                    tsx_listings.add_symbol(symbol, name, id_)
                    else:  
                        symbol = str(result.get('symbol', ''))
                        symbol = self.__convert_symbol_for_questrade__(symbol)
                        name = str(result.get('name', ''))
                        id_ = utils.lookup_symbol_id(symbol)
                        if id_ != -1:
                            tsx_listings.add_symbol(symbol, name, id_)
                        
                response = {"Message": "success"}
            else:
                response = {"Message": "No results"}
        
        except ValueError as e:
            response = {"ValueError": e}
    
        except TypeError as e:
            response = {"TypeError": e}
             
        except requests.exceptions.RequestException as e:
            response = {"RequestException": e}
            
        finally:
            return response
        
    def fetchAllListings(self):
        for o in self.search_options:
            self.fetchListings(o)
        tsx_listings.cleanup()
    
    def isValidListing(self, symbol):
        symbolId = utils.lookup_symbol_id(symbol)
        return symbolId != -1
    
    def __convert_symbol_for_questrade__(self, symbol):
        questrade_symbol = str(symbol)
        
        if '.DB.' in questrade_symbol:
            questrade_symbol = questrade_symbol.replace('.DB.','.DB')
        elif '.PR.' in questrade_symbol:
            questrade_symbol = questrade_symbol.replace('.PR.','.PR')
        elif '.PF.' in questrade_symbol:
            questrade_symbol = questrade_symbol.replace('.PF.','.PF')
        elif '.WT.' in questrade_symbol:
            questrade_symbol = questrade_symbol.replace('.WT.','.WT')
        
        questrade_symbol += '.TO'
        
        return questrade_symbol


def printDots(wait_time, stop_event):
    while (not stop_event.is_set()):
        print ".",
        stop_event.wait(wait_time)
        pass


if __name__ == '__main__':
    h = TSXListingHandler()
    
    print "=================================================="
    print "Begin fetching all TSX listings and perform validation"
    t1 = datetime.now()
    print "Start time: %s" % t1.isoformat()
    tr1 = Thread(target=h.fetchAllListings)
    tr1.daemon = True
    tr1.start()
    
    tr2_stop = Event()
    tr2 = Thread(target=printDots, args=(10, tr2_stop))
    tr2.daemon = True
    tr2.start()
    
    tr1.join()
    tr2_stop.set()
    
    n = tsx_listings.get_count()
    n_new = tsx_listings.get_new_count()
    n_updated = tsx_listings.get_updated_count()
    n_orphaned = tsx_listings.get_orphaned_count()
    
    t2 = datetime.now()
    tdelta = t2 - t1
    
    print "\n"
    print "End time: %s" % t2.isoformat()
    print "Total time: %s" % str(tdelta)
    print "\n"
    print "Total number of TSX listings: %u" % n
    print "New listings: %u" % n_new
    print "Updated listings: %u" % n_updated
    print "Orphaned listings: %u" % n_orphaned
    
    print "=================================================="
