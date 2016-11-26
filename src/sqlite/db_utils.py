'''
Created on Nov 25, 2016

@author: Peter
'''
import sqlite3
import os
import datetime
from sqlite3 import OperationalError


def is_symbol(symbol):
    conn = __conn_lookup_symbol_db__()
    exists = conn.execute('select count(*) from SYMBOL_IDS where SYMBOL = "%s"' % symbol.upper()).fetchone()[0] != 0
    conn.close()
    return exists


def get_symbol_id(symbol):
    conn = __conn_lookup_symbol_db__()
    cursor = conn.execute('select SYMBOL_ID from SYMBOL_IDS where SYMBOL = "%s"' % symbol.upper())
    row = cursor.fetchone()
    value = row[0] if row is not None else 'na'
    conn.close()
    return value


def add_symbol(symbol, symbol_id):
    if is_symbol(symbol):
        __update_symbol_table__(symbol, symbol_id)
    else:
        __insert_symbol_table__(symbol, symbol_id)


def __conn_lookup_symbol_db__():
    conn = sqlite3.connect(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'symbol_table.db'))
    try:
        conn.execute('select count(*) from SYMBOL_IDS')
    except OperationalError:
        __create_symbol_table__(conn)
    return conn


def __create_symbol_table__(conn):
    conn.execute('''create table if not exists  SYMBOL_IDS
                    (SYMBOL    TEXT PRIMARY KEY    NOT NULL,
                    SYMBOL_ID    TEXT    NOT NULL,
                    CREATE_SECS    INTEGER)''')


def __insert_symbol_table__(symbol, symbol_id):
    conn = __conn_lookup_symbol_db__()
    conn.execute('insert into SYMBOL_IDS(SYMBOL,SYMBOL_ID,CREATE_SECS) values("%s", "%s", %u)' % (symbol.upper(), symbol_id, __get_secs_since_epoch__()))
    conn.commit()
    conn.close()
    

def __update_symbol_table__(symbol, symbol_id):
    conn = __conn_lookup_symbol_db__()
    conn.execute('update SYMBOL_IDS set SYMBOL_ID = "%s", CREATE_SECS = %u where SYMBOL = "%s"' % (symbol_id, __get_secs_since_epoch__(), symbol.upper()))
    conn.commit()
    conn.close()
    

def __delete_symbol_table__(symbol):
    conn = __conn_lookup_symbol_db__()
    conn.execute('delete from SYMBOL_IDS where SYMBOL = "%s"' % symbol.upper())
    conn.commit()
    conn.close()
    

def __select_symbol_table__():
    conn = __conn_lookup_symbol_db__()
    for row in conn.execute('select SYMBOL,SYMBOL_ID,CREATE_SECS from SYMBOL_IDS'):
        print 'SYM = %s' % row[0]
        print 'SYM_ID = %s' % row[1]
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
    conn = __conn_lookup_symbol_db__()
    conn.close()
