'''Questrade Enumerations

@summary: An enumerations module to mimic the enumerations documented by Questrade

@see http://www.questrade.com/api/documentation/rest-operations/enumerations/enumerations

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

class Currency:
    USD = 'USD'
    CAD = 'CAD'


class Exchange:
    TSX = 'TSX'
    TSXV = 'TSXV'
    CNSX = 'CNSX'
    MX = 'MX'
    NASDAQ = 'NASDAQ'
    NYSE = 'NYSE'
    AMEX = 'AMEX'
    ARCA = 'ARCA'
    OPRA = 'OPRA'
    PinkSheets = 'PinkSheets'
    OTCBB = 'OTCBB'


class OrderStateFilterType:
    All = 'All'
    Open = 'Open'
    Closed = 'Closed'
    

class OrderAction:
    Buy = 'Buy'
    Sell = 'Sell'


class OrderSide:
    Buy = 'Buy'
    Sell = 'Sell'
    Short = 'Short'
    Cov = 'Cov'
    BTO = 'BTO'
    STC = 'STC'
    STO = 'STO'
    BTC = 'BTC'

 
class HistoricalDataGranularity:
    OneMinute = 'OneMinute'
    TwoMinutes = 'TwoMinutes'
    ThreeMinutes = 'ThreeMinutes'    
    FourMinutes = 'FourMinutes'
    FiveMinutes = 'FiveMinutes'
    TenMinutes = 'TenMinutes'
    FifteenMinutes = 'FifteenMinutes'
    TwentyMinutes = 'TwentyMinutes'
    HalfHour = 'HalfHour'
    OneHour = 'OneHour'
    TwoHours = 'TwoHours'
    FourHours = 'FourHours'
    OneDay = 'OneDay'
    OneWeek = 'OneWeek'
    OneMonth = 'OneMonth'
    OneYear = 'OneYear'


class OptionType:
    Call = 'Call'
    Put = 'Put'

