'''Mediator

@summary: An RTD Mediator that orchestrates the interaction between
    IQStreamer, RTDStreamObserver and RTDMessageQueue.

@see: http://www.questrade.com/api/documentation/streaming

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
from questrade.api.streamer.IQStreamer import IQStreamer
from RTDStreamObserver import RTDStreamObserver
from rtd.RTDMessageQueue import RTDMessageQueue


class Mediator(object):

    dict_rtds = {}
    _streaming_thread = None
    
    @staticmethod
    def add_message_queue(symbol, header):
        _id = utils.lookup_symbol_id(symbol)
        tup = (_id, symbol, header)
        
        mq_name = symbol + '_' + header
        mq = RTDMessageQueue(mq_name)
        Mediator.dict_rtds[tup] = mq
        
        if Mediator._streaming_thread is None: 
            Mediator._streaming_thread = IQStreamer.run_in_thread('markets/quotes', {'ids': Mediator.get_mq_ids_as_str()}, (RTDStreamObserver(Mediator.dict_rtds),))
            Mediator._streaming_thread.start()
        else:
            IQStreamer.create_socket('markets/quotes', {'ids': Mediator.get_mq_ids_as_str()})
        
    @staticmethod
    def remove_message_queue(symbol, header):
        _id = utils.lookup_symbol_id(symbol)
        tup = (_id, symbol, header)
        keys = (k for (k, v) in Mediator.dict_rtds.items() if k == tup)
        for k in keys:
            Mediator.dict_rtds.pop(k)
    
    @staticmethod
    def get_mqs_by_id(_id):
        return (v for (k, v) in Mediator.dict_rtds.items() if k[0] == _id)
    
    @staticmethod
    def get_mqs_by_symbol(symbol):
        return (v for (k, v) in Mediator.dict_rtds.items() if k[1] == symbol)
        
    @staticmethod
    def get_mq_ids():
        s = set()
        for t in Mediator.dict_rtds.keys():
            s.add(t[0])
        return s
    
    @staticmethod
    def get_mq_ids_as_str():
        _str = ''
        for s in Mediator.get_mq_ids():
            _str += str(s) + ','
        if _str.endswith(','):
            _str = _str[:-1]
        return _str
