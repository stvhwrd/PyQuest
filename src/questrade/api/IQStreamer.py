'''Streaming Data

@summary: An implementation of Questrade's Streaming services. Capable of
   performing the initial authorization handshake with Questrade servers,
   obtaining a port and opening a WebSocket to retreive streaming data
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
import sys

from twisted.python import log
from twisted.internet import reactor, ssl

from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from questrade.token import token_ops
from questrade.api import utils


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
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        
    @staticmethod
    def createWebSocket(api, params=None):
        log.startLogging(sys.stdout)
        
        if params == None:
            params = {'stream': 'true', 'mode': 'WebSocket'}
        elif 'stream' in params and 'mode' in params:
            pass
        else:
            params.update({'stream': 'true', 'mode': 'WebSocket'})
        
        r = utils.call_api(api, params)
        
        if 'streamPort' in r:
            web_protocol = 'https://'
            socket_protocol = 'wss://'
            api_server = token_ops.get_api_server()
            if api_server != None:
                api_server = api_server.replace(web_protocol, socket_protocol)
                if api_server.endswith('/'):
                    api_server = api_server[:-1]
            
            stream_port = str(r.get('streamPort'))
            url = api_server + ':' + stream_port
            
            print('WebSocket port obtained: %s' % stream_port)
            print('Establishing socket connection through %s' % url)
            
            factory = WebSocketClientFactory(url)
            factory.protocol = IQStreamer
        
            if factory.isSecure:
                contextFactory = ssl.ClientContextFactory()
            else:
                contextFactory = None
        
            connectWS(factory, contextFactory)
            reactor.run()


if __name__ == '__main__':
    params = {'ids': 8049}
    api = 'markets/quotes'
    IQStreamer.createWebSocket(api, params)
