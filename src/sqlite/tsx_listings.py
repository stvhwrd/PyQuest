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
from sqlite3 import OperationalError
from utils import datetime_utils

table_name = 'tsx_listings.db'


def symbol_exists(symbol):
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

def get_symbol_id(symbol):
    conn = __conn_db__()
    cursor = conn.execute('select ID from TSX_LISTINGS where SYMBOL = "%s"' % symbol.upper())
    row = cursor.fetchone()
    value = row[0] if row is not None else '-1'
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

def get_symbol_ids():
    conn = __conn_db__()
    cursor = conn.execute('select ID from TSX_LISTINGS')
    rows = cursor.fetchall()
    ids = []
    for row in rows:
        ids.append(row[0])
    conn.close()
    return ids

def get_symbols_asJSON():
    conn = __conn_db__()
    cursor = conn.execute('select SYMBOL,ID,NAME from TSX_LISTINGS')
    rows = cursor.fetchall()
    data = {}
    results = data['results'] = []
    for row in rows:
        symbol = str(row[0])
        id_ = str(row[1])
        name = str(row[2])
        results.append({'symbol': symbol, 'id': id_, 'name': name})
    conn.close()
    data['length'] = len(results)
    return json.loads(json.dumps(data))

def add_symbol(symbol, name, id_=None):
    if symbol_exists(symbol):
        __update_table__(symbol, name, id_)
    else:
        __insert_table__(symbol, name, id_)

def get_count():
    conn = __conn_db__()
    count = conn.execute('select count(*) from TSX_LISTINGS').fetchone()[0]
    conn.close()
    return count

def get_new_count():
    conn = __conn_db__()
    count = conn.execute('select count(*) from TSX_LISTINGS where DATETIME(CREATE_TS) == DATETIME(UPDATE_TS)').fetchone()[0]
    conn.close()
    return count

def get_updated_count():
    conn = __conn_db__()
    count = conn.execute('select count(*) from TSX_LISTINGS where DATETIME(CREATE_TS) < DATETIME(UPDATE_TS)').fetchone()[0]
    conn.close()
    return count

def get_orphaned_count():
    conn = __conn_db__()
    count = conn.execute('select count(*) from TSX_LISTINGS where DATE(CREATE_TS) < DATE(UPDATE_TS) AND DATE(UPDATE_TS) < (SELECT MAX(DATE(UPDATE_TS)))').fetchone()[0]
    conn.close()
    return count

def cleanup():
    conn = __conn_db__()
    conn.execute('delete from TSX_LISTINGS where ID = -1')
    conn.execute('delete from TSX_LISTINGS where DATE(CREATE_TS) < DATE(UPDATE_TS) AND DATE(UPDATE_TS) < (SELECT MAX(DATE(UPDATE_TS)))')
    conn.close()

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
                    ID    TEXT    NOT NULL,
                    NAME    TEXT    NOT NULL,
                    CREATE_TS    TIMESTAMP,
                    UPDATE_TS    TIMESTAMP)''')


def __insert_table__(symbol, name, id_="-1"):
    if id_ is None:
        id_ = "-1"
    conn = __conn_db__()
    now = datetime_utils.datetime_now()
    conn.execute('insert into TSX_LISTINGS(SYMBOL,ID,NAME,CREATE_TS,UPDATE_TS) values(?, ?, ?, ?,?)', (symbol.upper(), id_, name, now, now))
    conn.commit()
    conn.close()
    

def __update_table__(symbol, name, id_="-1"):
    if id_ is None:
        id_ = "-1"
    conn = __conn_db__()
    conn.execute('update TSX_LISTINGS set ID = ?, NAME = ?, UPDATE_TS = ? where SYMBOL = ?', (id_, name, datetime_utils.datetime_now(), symbol.upper()))
    conn.commit()
    conn.close()
    

def __delete_table__(symbol):
    conn = __conn_db__()
    conn.execute('delete from TSX_LISTINGS where SYMBOL = "%s"' % symbol.upper())
    conn.commit()
    conn.close()
    

def __select_table__():
    conn = __conn_db__()
    for row in conn.execute('select SYMBOL,ID,NAME,CREATE_TS,UPDATE_TS from TSX_LISTINGS'):
        print 'SYM = %s, ID = %s, NAME = %s, CREATE_TS = %s, UPDATE_TS = %s' % (row[0], row[1], row[2], row[3], row[4])
    conn.close()


if __name__ == '__main__':
    print get_symbols_asJSON()
