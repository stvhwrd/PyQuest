'''TSXHandler

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


class TSXHandler(object):

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
                    if 'instruments' in s:
                        instruments = result.get('instruments')
                        for i in instruments:
                            symbol = str(i.get('symbol', ''))
                            symbol = self.__convert_symbol_for_questrade__(symbol)
                            name = str(i.get('name', ''))
                            if self.isValidListing(symbol):
                                tsx_listings.add_symbol(symbol, name)
                    else:
                        symbol = result.get('symbol', '')
                        symbol = self.__convert_symbol_for_questrade__(symbol)
                        name = result.get('name', '')
                        if self.isValidListing(symbol):
                            tsx_listings.add_symbol(symbol, name)
        
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


if __name__ == '__main__':
    h = TSXHandler()
    h.fetchAllListings()
    
    