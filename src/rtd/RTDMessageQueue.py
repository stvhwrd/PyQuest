'''RTDMessageQueue

@summary: A first-class object representing the ctypes API's exposed in the
    MessageQueue.RTDServer.dll.

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

import ctypes
import rtd_ctypes_header as rtd

class RTDMessageQueue(object):
    
    def __init__(self, name):
        self.name = name
        
    def open(self):
        try:
            rtd.mq_open(self.name)
        except:
            pass
    
    def close(self):
        try:
            rtd.mq_close(self.name)
        except:
            pass
    
    def send(self, message):
        try:
            rtd.mq_send(self.name, str(message))
        except:
            pass
        
    def receive(self):
        try:
            char_p = ctypes.c_char_p()
            rtd.mq_recv(self.name, char_p)
            return char_p.value
        except:
            pass
