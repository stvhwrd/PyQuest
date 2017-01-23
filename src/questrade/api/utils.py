'''Questrade API Utility module

@summary: A utility module to make common Restful API calls.

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

import questrade.token.token_ops as token_ops
import sqlite.db_utils as db_utils
import configparser as Config
import os
import json
import requests
import logging
from datetime import datetime, date, time
from dateutil.tz import tzlocal


config = Config.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))
api_version = config.get('Questrade', 'api_version')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'questrade.log'), level=logging.DEBUG)
logger = logging.getLogger('questrade')


def get_valid_token():
    token = token_ops.get_token()
    
    # If token expired, get a new one
    if token_ops.is_token_expired(token):
        # First try to use the refresh token to get a new access token
        if token_ops.is_valid_token(token):
            token = token_ops.refresh_token(token['refresh_token'])
            
        # If the token is not valid after the refresh, force a new token
        if not token_ops.is_valid_token(token):
            token = token_ops.get_token(new=True)
    
    return token


def get_base_uri(token):
    api_server = token_ops.get_api_server(token)
    return api_server + api_version


def call_api(api, params=None):
    token = get_valid_token()
    if token == None:
        response = {'message': 'no token'}
        logging.info(json.dumps(response))
        return response
    
    authorization_value = token_ops.get_token_type(token) + ' ' + token_ops.get_access_token(token)
    headers = {'Authorization': authorization_value}
    
    uri = get_base_uri(token) + api
    
    http_verb = "GET"
    
    response = {}
    
    try:
        logging.info('>>>>>>>> SENDING >>>>>>>>')
        logging.info('Headers:\t' + json.dumps(headers))
        logging.info('Params: \t' + json.dumps(params))
        logging.info('Calling:\t' + http_verb + ' ' + uri)
        logging.info('>>>>>>>>>>>>>>>>>>>>>>>>>')
        
        r = requests.get(uri, headers=headers, params=params)
        response = r.json()
            
    except ValueError as e:
        response = {"ValueError": e}
    
    except TypeError as e:
        response = {"TypeError": e}
         
    except requests.exceptions.RequestException as e:
        response = {"RequestException": e}
        
    finally:
        logging.info('<<<<<<<< RECEIVING <<<<<<')
        logging.info('Headers:\t' + str(r.headers))
        logging.info('Body:   \t' + json.dumps(response))
        logging.info('<<<<<<<<<<<<<<<<<<<<<<<<<')
        
        return response


def lookup_symbol_id(symbol):
    symbol_id = -1
    
    if isinstance(symbol, (int)):
        return symbol

    if db_utils.is_symbol(symbol):
        symbol_id = db_utils.get_symbol_id(symbol)
    else:
        params = {'prefix': symbol,
                  'offset': 0}
        r = call_api('symbols/search', params)
        
        stocks = r.get('symbols')
        if len(stocks) > 0:
            stock = stocks[0]
            if 'symbolId' in stock:
                symbol_id = stock.get('symbolId')
                db_utils.add_symbol(symbol, symbol_id)
    
    return symbol_id


def lookup_symbol_ids(symbols):
    ids = []
    for s in symbols:
        ids.append(lookup_symbol_id(s))
    
    return ids


def iso_today():
    today = date.today()
    return today.isoformat()


def iso_time():
    return time.isoformat()


def iso_now():
    now = datetime.now(tzlocal())
    return now.isoformat()
