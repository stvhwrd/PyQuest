'''RTD Stream Observer

@summary: An Observer in the Publish/Subscriber design pattern.  This
    observer sends the JSON object to a RTD Message Queue.

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

from questrade.api.streamer.Observer import Observer
import json


class RTDStreamObserver(Observer):
    
    def __init__(self, dict_rtds):
        self.dict_rtds = dict_rtds
    
    
    def update(self, payload, isBinary):
        if not isBinary and payload is not None:
            s = payload.decode('utf8')
            j = json.loads(s)
            
            if 'quotes' in j:
                quotes = j.get('quotes')
                for q in quotes:
                    symbol = q.get('symbol', '_na_')
                    if symbol != '_na_':
                        self.send_message(symbol, q)
                        
    
    def send_message(self, symbol, quote):
        items = ( (k, v) for (k, v) in self.dict_rtds.items() if k[1] == symbol )
        for item in items:
            header = item[0][2]
            mq = item[1]
            v = quote.get(header, '_na_')
            if v != '_na_':
                mq.send(v)
                