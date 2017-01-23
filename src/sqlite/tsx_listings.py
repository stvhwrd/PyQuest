'''TSX Listings

@summary: A set of functions that help to store and retrieve TSX Listings


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

import sqlite3
import os
import json
import datetime
from sqlite3 import OperationalError

table_name = 'tsx_listings.db'


def is_symbol(symbol):
    conn = __conn_db__()
    exists = conn.execute('select count(*) from TSX_LISTINGS where SYMBOL = "%s"' % symbol.upper()).fetchone()[0] != 0
    conn.close()
    return exists

def get_symbol_name(symbol):
    conn = __conn_db__()
    cursor = conn.execute('select NAME from TSX_LISTINGS where SYMBOL = "%s"' % symbol.upper())
    row = cursor.fetchone()
    value = row[0] if row is not None else 'na'
    conn.close()
    return value

def get_symbol_names():
    conn = __conn_db__()
    cursor = conn.execute('select NAME from TSX_LISTINGS')
    rows = cursor.fetchall()
    names = []
    for row in rows:
        names.append(row[0])
    conn.close()
    return names

def get_symbols():
    conn = __conn_db__()
    cursor = conn.execute('select SYMBOL from TSX_LISTINGS')
    rows = cursor.fetchall()
    symbols = []
    for row in rows:
        symbols.append(row[0])
    conn.close()
    return symbols

def get_symbols_asJSON():
    conn = __conn_db__()
    cursor = conn.execute('select SYMBOL,NAME from TSX_LISTINGS')
    rows = cursor.fetchall()
    data = {}
    results = data['results'] = []
    for row in rows:
        symbol = str(row[0])
        name = str(row[1])
        results.append({'symbol': symbol, 'name': name})
    conn.close()
    data['length'] = len(results)
    return json.loads(json.dumps(data))

def add_symbol(symbol, name):
    if is_symbol(symbol):
        __update_table__(symbol, name)
    else:
        __insert_table__(symbol, name)

def get_count():
    conn = __conn_db__()
    count = conn.execute('select count(*) from TSX_LISTINGS').fetchone()[0]
    conn.close()
    return count

def __conn_db__():
    conn = sqlite3.connect(os.path.join(os.path.abspath(os.path.dirname(__file__)), table_name))
    try:
        conn.execute('select count(*) from TSX_LISTINGS')
    except OperationalError:
        __create_table__(conn)
    return conn


def __create_table__(conn):
    conn.execute('''create table if not exists  TSX_LISTINGS
                    (SYMBOL    TEXT PRIMARY KEY    NOT NULL,
                    NAME    TEXT    NOT NULL,
                    CREATE_SECS    INTEGER)''')


def __insert_table__(symbol, name):
    conn = __conn_db__()
    conn.execute('insert into TSX_LISTINGS(SYMBOL,NAME,CREATE_SECS) values("%s", "%s", %u)' % (symbol.upper(), name, __get_secs_since_epoch__()))
    conn.commit()
    conn.close()
    

def __update_table__(symbol, name):
    conn = __conn_db__()
    conn.execute('update TSX_LISTINGS set NAME = "%s", CREATE_SECS = %u where SYMBOL = "%s"' % (name, __get_secs_since_epoch__(), symbol.upper()))
    conn.commit()
    conn.close()
    

def __delete_table__(symbol):
    conn = __conn_db__()
    conn.execute('delete from TSX_LISTINGS where SYMBOL = "%s"' % symbol.upper())
    conn.commit()
    conn.close()
    

def __select_table__():
    conn = __conn_db__()
    for row in conn.execute('select SYMBOL,NAME,CREATE_SECS from TSX_LISTINGS'):
        print 'SYM = %s' % row[0]
        print 'NAME = %s' % row[1]
        print 'CREATE_SECS = %s' % row[2]
    conn.close()


def __get_secs_since_epoch__():
    epoch = datetime.datetime.utcfromtimestamp(0)
    now = datetime.datetime.utcnow()
    delta = now - epoch
    return delta.total_seconds()


def __get_datetime_from_secs__(seconds):
    return datetime.datetime.utcfromtimestamp(seconds)


if __name__ == '__main__':
    #print get_symbols()
    #print get_symbol_names()
    j = get_symbols_asJSON()
    print j.get('length')
