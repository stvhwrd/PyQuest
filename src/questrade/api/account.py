'''Questrade API Wrapper - Account calls

@summary: A wrapper for the Questrade Account Restful APIs

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
import questrade.api.enumerations as enums


__api_ops__ = {
    'time': 'time',
    'accounts': 'accounts',
    'positions': 'accounts/{0}/positions',
    'balances': 'accounts/{0}/balances',
    'executions': 'accounts/{0}/executions',
    'orders': 'accounts/{0}/orders',
    'activities': 'accounts/{0}/activities',
}


def time():
    '''
    Retrieves current server time.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/account-calls/time
    '''
    return utils.call_api(__api_ops__['time'])


def accounts():
    '''
    Retrieves the accounts associated with the user on behalf of which the API client is authorized.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/account-calls/accounts
    '''
    return utils.call_api(__api_ops__['accounts'])


def accounts_positions(id_):
    '''
    Retrieves positions in a specified account.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-positions
    '''
    return utils.call_api(__api_ops__['positions'].format(id_))


def accounts_balances(id_):
    '''
    Retrieves per-currency and combined balances for a specified account.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-balances
    '''
    return utils.call_api(__api_ops__['balances'].format(id_))


def accounts_executions(id_, start_time=None, end_time=None):
    '''
    Retrieves executions for a specific account.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-executions
    '''
    if start_time == None:
        start_time = utils.iso_now()
    if end_time == None:
        end_time = utils.iso_now()
    
    params = {'startTime': start_time,
              'endTime': end_time}
    return utils.call_api(__api_ops__['executions'].format(id_), params)


def accounts_orders(id_, start_time=None, end_time=None, state_filter=None, order_id=0):
    '''
    Retrieves orders for specified account
    
    @see: http://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-orders
    '''
    if start_time == None:
        start_time = utils.iso_now()
    if end_time == None:
        end_time = utils.iso_now()
    if state_filter == None:
        state_filter = enums.OrderStateFilterType.All
    
    params = {'startTime': start_time,
              'endTime': end_time,
              'stateFilter': state_filter,
              'orderId': order_id}
    return utils.call_api(__api_ops__['orders'].format(id_), params)


def accounts_activities(id_, start_time=None, end_time=None):
    '''
    Retrieve account activities, including cash transactions, dividends, trades, etc.
    
    @see: http://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-activities
    '''
    if start_time == None:
        start_time = utils.iso_now()
    if end_time == None:
        end_time = utils.iso_now()
    
    params = {'startTime': start_time,
              'endTime': end_time}
    return utils.call_api(__api_ops__['activities'].format(id_), params)


if __name__ == '__main__':
    time()
