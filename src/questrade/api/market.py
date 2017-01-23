'''Questrade API Wrapper - Market calls

@summary: A wrapper for the Questrade Market Restful APIs

@see: http://www.questrade.com/api/documentation/getting-started

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

import questrade.api.utils as utils
import questrade.api.enumerations as enumerations


__api_ops__ = {
    'symbol': 'symbols/{0}',
    'symbols': 'symbols',
    'search': 'symbols/search',
    'options': 'symbols/{0}/options',
    'markets': 'markets',
    'quote': 'markets/quotes/{0}',
    'quotes': 'markets/quotes',
    'moptions': 'markets/quotes/options',
    'strategies': 'markets/quotes/strategies',
    'candles': 'markets/candles/{0}',
}


def symbol(id_):
    '''
    Retrieves detailed information about one symbol.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-id
    '''
    return utils.call_api(__api_ops__['symbol'].format(id_))


def symbolIds(ids):
    '''
    Retrieves detailed information about one or more symbols.
    @note: ids must be a list or comma separated string
    
    @see:  http://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-id
    '''
    syms = ''
    if isinstance(ids, list):
        for s in ids:
            syms += str(s) +','
        syms = syms[:-1]  # remove last ,
    else:
        syms = ids
        
    params = {'ids': syms}
    return utils.call_api(__api_ops__['symbols'], params)


def symbolNames(names):
    '''
    Retrieves detailed information about one or more symbols.
    @note: names must be a list or comma separated string
    
    @see:  http://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-id
    '''
    syms = ''
    if isinstance(names, list):
        for s in names:
            syms += str(s) + ','
        syms = syms[:-1]  # remove last ,
    else:
        syms = names
        
    params = {'names': syms}
    return utils.call_api(__api_ops__['symbols'], params)


def symbols_search(prefix, offset='0'):
    '''
    Retrieves symbol(s) using several search criteria.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-search
    '''
    params = {'prefix': prefix,
              'offset': offset}
    return utils.call_api(__api_ops__['search'], params)


def symbols_options(id_):
    '''
    Retrieves an option chain for a particular underlying symbol.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-id-options
    '''
    return utils.call_api(__api_ops__['options'].format(id_))


def markets():
    '''
    Retrieves information about supported markets.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/market-calls/markets
    '''
    return utils.call_api(__api_ops__['markets'])


def markets_quote(id_):
    '''
    Retrieves a single Level 1 market data quote for one symbol.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/market-calls/markets-quotes-id
    '''
    return utils.call_api(__api_ops__['quote'].format(id_))


def markets_quotes(ids):
    '''
    Retrieves a single Level 1 market data quote for one or more symbols.
    @note: ids must be a list or comma separated string
    
    @see: http://www.questrade.com/api/documentation/rest-operations/market-calls/markets-quotes-id
    '''
    syms = []
    if isinstance(ids, basestring):
        syms = syms.split(',')
    else:
        syms = ids
    
    result = {'quotes': []}
    
    arry_chunks = __array_chunks(syms, 200)
    for ids_array in arry_chunks:
        ids_str = ''
        for s in ids_array:
            ids_str += str(s) + ','
        ids_str = ids_str[:-1]  # remove last ,
        
        params = {'ids': ids_str}
        r = utils.call_api(__api_ops__['quotes'], params)
        if 'quotes' in r:
            result['quotes'] = result['quotes'] + r.get('quotes')
    
    return result


def markets_quotes_options(option_id_filters, ids):
    '''
    Retrieves a single Level 1 market data quote and Greek data for one or more option symbols.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/market-calls/markets-quotes-options
    @todo: Need to finish implementation
    '''
    params = {'filters': option_id_filters,
              'ids': ids}
    return utils.call_api(__api_ops__['moptions'], params)


def markets_quotes_strategies():
    '''
    Retrieve a calculated L1 market data quote for a single or many multi-leg strategies
    
    @see: http://www.questrade.com/api/documentation/rest-operations/market-calls/markets-quotes-strategies
    @todo: Need to finish implementation
    '''
    return utils.call_api(__api_ops__['strategies'])


def markets_candles(id_, start_time=None, end_time=None, interval=None):
    '''
    Retrieves historical market data in the form of OHLC candlesticks for a specified symbol.
    This call is limited to returning 2,000 candlesticks in a single response.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/market-calls/markets-candles-id
    '''
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


def __array_chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in xrange(0, len(l), n))


if __name__ == '__main__':
    markets_quotes('8049')
