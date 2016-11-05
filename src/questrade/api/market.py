'''Questrade API Wrapper - Market calls

@summary: A wrapper for the Questrade Market Restful APIs

@see http://www.questrade.com/api/documentation/getting-started

@copyright: 2016
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

import utils
from questrade.api import enumerations


__api_ops__ = {
    'symbols': 'symbols/{0}',
    'search': 'symbols/search',
    'options': 'symbols/{0}/options',
    'markets': 'markets',
    'options': 'markets/quotes/options',
    'strategies': 'markets/quotes/strategies',
    'candles': 'markets/candles/{0}',
}


def symbols(id_):
    return utils.call_api(__api_ops__['symbols'].format(id_))

def symbols_search(prefix, offset='0'):
    params = {'prefix': prefix,
              'offset': offset}
    return utils.call_api(__api_ops__['search'], params)

def symbols_options(id_):
    return utils.call_api(__api_ops__['options'].format(id_))

def markets():
    return utils.call_api(__api_ops__['markets'])

def markets_quotes(id_):
    return utils.call_api(__api_ops__['quotes'].format(id_))

def markets_quotes_options(option_id_filters, ids):
    params = {'filters': option_id_filters,
              'ids': ids}
    return utils.call_api(__api_ops__['options'], params)

def markets_candles(id_, start_time=None, end_time=None, interval=None):
    if start_time == None:
        start_time = utils.iso_now()
    if end_time == None:
        end_time = utils.iso_now()
    if interval == None:
        interval = enumerations.HistoricalDataGranularity.FiveMinutes
    
    params = {'startTime': start_time,
              'endTime': end_time,
              'interval': interval}
    return utils.call_api(__api_ops__['candles'].format(id_), params)



if __name__ == '__main__':
    symbols('8049')
