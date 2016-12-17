'''Streaming Data

@summary: An implementation of Questrade's Streaming services. Capable of
   performing the initial authorization handshake with Questrade servers,
   obtaining a port and opening a WebSocket to retrieve streaming data
   from the port.

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

from twisted.internet import reactor
from twisted.internet import error
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from questrade.token import token_ops
from StreamObserver import StreamObserver
from StreamPublisher import StreamPublisher
from threading import Thread

import questrade.api.utils as utils

import logging
logger = logging.getLogger('questrade')

class IQStreamer(WebSocketClientProtocol):
    
    def sendAccessToken(self):
        access_token = token_ops.get_access_token()
        if access_token != None:
            self.sendMessage(access_token.encode('utf8'))
        else:
            self.sendMessage('No access token'.encode('utf8'))

    def onOpen(self):
        self.sendAccessToken()

    def onMessage(self, payload, isBinary):
        StreamPublisher.onMessage(payload, isBinary)


    @staticmethod
    def _params_streaming(params):
        if params is None:
            params = {'stream': 'true', 'mode': 'WebSocket'}
        elif 'stream' in params and 'mode' in params:
            pass
        else:
            params.update({'stream': 'true', 'mode': 'WebSocket'})
        return params

    @staticmethod
    def create_socket(api, params=None):
        r = utils.call_api(api, IQStreamer._params_streaming(params))
        
        if 'streamPort' in r:
            stream_port = r.get('streamPort')
        else:
            stream_port = None
        
        return stream_port
        
    @staticmethod
    def connect_to_socket(port, observers=None):
        if port is None:
            raise ValueError('port', port)
        
        api_server = token_ops.get_api_server()
        if api_server is not None:
            if api_server.startswith('https://'):
                api_server = api_server.replace('https://', 'wss://')
            if api_server.endswith('/'):
                api_server = api_server[:-1]
        
            url = api_server + ':' + str(port)
            
            logging.info('connect_to_socket')
            logging.info('Establishing socket connection:  %s' % url)
            
            factory = WebSocketClientFactory(url)
            factory.protocol = IQStreamer
            
            connectWS(factory)
            
            if observers is not None:
                publisher = StreamPublisher()
                for obs in observers:
                    publisher.register(obs)
            
            try:
                factory.reactor.run(installSignalHandlers=False)
            except error.ReactorAlreadyRunning:
                pass

    @staticmethod
    def connect(api, params=None, observers=None):
        if observers is None:
            observers = (StreamObserver(),)
        IQStreamer.connect_to_socket(IQStreamer.create_socket(api, params), observers)
    
    @staticmethod
    def run_in_thread(api, params=None, observers=None):
        t = Thread(target=IQStreamer.connect, args=(api, params, observers))
        t.setDaemon(True)
        return t
    
    @staticmethod
    def disconnect_from_thread():
        reactor.callFromThread(reactor.stop)


if __name__ == '__main__':
    import time
    
    IQStreamer.run_in_thread('markets/quotes', {'ids': '8049'}).start()
   
    time.sleep(3)
    IQStreamer.create_socket('markets/quotes', {'ids': '8049,23364'})
    
    time.sleep(3)
    IQStreamer.run_in_thread('markets/quotes', {'ids': '8049'}).start()
    
    time.sleep(3)
    IQStreamer.disconnect_from_thread()
    
    
    
    