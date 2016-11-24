'''User Defined Functions

@summary: XLWings Implementation of Questrade User Defined Functions

@see: http://www.questrade.com/api/documentation/getting-started
@see: https://www.xlwings.org/

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

import xlwings as xw
import os
import datetime
import dateutil.parser
import questrade.api.account as api_account
from questrade.api import market as api_market
from tinydb import TinyDB, Query

__lookup_symbol_table__ = TinyDB(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'symbol_table.json'))
__date_conversion_keys__ = ('time', 'dividendDate', 'exDate', 'extendedStartTime', 'extendedEndTime', 'startTime', 'endTime', 'start', 'end')
__unavailable_data__ = 'na'


@xw.func
def xw_GetServerTime():
    r = api_account.time()
    t = r.get('time')
    return xw_isoDateTimeToExcel(t)


@xw.func
def xw_GetAccountsUserid():
    r = api_account.accounts()
    return r.get('userId')


@xw.func
@xw.arg('headers', ndim=1)
@xw.ret(expand='table')
def xw_GetAccounts(headers):
    r = api_account.accounts()
    accounts = r.get('accounts')
    
    return __table__(accounts, headers)


@xw.func
@xw.arg('accountId')
@xw.arg('headers', ndim=1)
@xw.ret(expand='table')
def xw_GetAccountPositions(accountId, headers):   
    r = api_account.accounts_positions(accountId)
    positions = r.get('positions')
    
    return __table__(positions, headers)


@xw.func
@xw.arg('headers', ndim=1)
@xw.ret(expand='table')
def xw_GetMarkets(headers):    
    r = api_market.markets()
    markets = r.get('markets')
    
    return __table__(markets, headers)


@xw.func
@xw.arg('symbols', ndim=1)
@xw.arg('headers', ndim=1)
@xw.ret(expand='table')
def xw_GetStocks(symbols, headers):
    r = api_market.symbolNames(symbols)
    stocks = r.get('symbols')
    
    return __table__(stocks, headers)


@xw.func
@xw.arg('symbols', ndim=1)
@xw.arg('headers', ndim=1)
@xw.ret(expand='table')
def xw_GetQuotes(symbols, headers):
    ids = xw_LookupSymbolIds(symbols)
    r = api_market.markets_quotes(ids)
    stocks = r.get('quotes')
    
    return __table__(stocks, headers)


@xw.func
@xw.arg('symbol')
@xw.arg('start_time')
@xw.arg('end_time')
@xw.arg('interval')
@xw.arg('headers', ndim=1)
@xw.ret(expand='table')
def xw_GetCandles(symbol, start_time, end_time, interval, headers):
    symbol_id = xw_LookupSymbolId(symbol)
    r = api_market.markets_candles(symbol_id, start_time, end_time, interval)
    candles = r.get('candles')
    
    return __table__(candles, headers)


def __table__(l, h):
    result = []
    for i in l:
        r = []
        for j in h:
            v = i.get(j, __unavailable_data__)
            if j in __date_conversion_keys__:
                v = xw_isoDateTimeToExcel(v)
            r.append(v)
        
        result.append(r)
    
    return result
    

@xw.func
@xw.arg('symbol')
def xw_GetStockId(symbol):
    return xw_LookupSymbolId(symbol)


@xw.func
@xw.arg('symbol')
def xw_LookupSymbolId(symbol):
    if isinstance(symbol, (int)):
        return symbol
    
    q = Query()
    records = __lookup_symbol_table__.search(q.symbol == symbol)
    
    if records == []:
        r = api_market.symbols_search(symbol)
        stocks = r.get('symbols')
        if len(stocks) > 0:
            stock = stocks[0]
            if 'symbolId' in stock:
                symbol_id = stock.get('symbolId')
                __lookup_symbol_table__.insert({'symbol_id': symbol_id, 'symbol': symbol})
                
    elif len(records) > 0:
        record = records[0]
        symbol_id = record.get('symbol_id')
            
    return symbol_id


@xw.func
@xw.arg('symbols', ndim=1)
@xw.ret(expand='right')
def xw_LookupSymbolIds(symbols):
    ids = []
    for s in symbols:
        ids.append(xw_LookupSymbolId(s))
    
    return ids   


@xw.func
def xw_isoDateTimeToExcel(dt):
    if dt == None:
        return ''
    elif dt == '':
        return ''
    
    reference_day = datetime.datetime(1900, 1, 1)
    
    input_day = dateutil.parser.parse(dt)
    input_day = input_day.replace(tzinfo=None)
    
    delta_days = (input_day - reference_day).days + 2  # Add 2 because excel start date is 1900-01-00 (not 1900-01-01) and need to add 1 for the sub arithmetic
    
    input_time = str(input_day.time())
    input_secs = sum(float(x) * 60.0 ** i for i, x in enumerate(reversed(input_time.split(":"))))
    
    input_secs_pct_of_day = input_secs / 86400.0
    
    return delta_days + input_secs_pct_of_day
