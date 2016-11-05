'''Questrade API Wrapper - Account calls

@summary: A wrapper for the Questrade Account Restful APIs

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
    return utils.call_api(__api_ops__['time'])

def accounts():
    return utils.call_api(__api_ops__['accounts'])

def accounts_positions(id_):
    return utils.call_api(__api_ops__['positions'].format(id_))

def accounts_balances(id_):
    return utils.call_api(__api_ops__['balances'].format(id_))

def accounts_executions(id_):
    return utils.call_api(__api_ops__['executions'].format(id_))

def accounts_orders(id_):
    return utils.call_api(__api_ops__['orders'].format(id_))

def accounts_activities(id_, start_time=None, end_time=None):
    if start_time == None:
        start_time = utils.iso_now()
    if end_time == None:
        end_time = utils.iso_now()
    
    params = {'startTime': start_time,
              'endTime': end_time}
    return utils.call_api(__api_ops__['activities'].format(id_), params)


if __name__ == '__main__':
    time()
