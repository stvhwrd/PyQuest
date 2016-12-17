'''rtd_ctypes_header

@summary: A header-type file to load and expose the MessageQueueRTDServer.dll API
    ctypes in Python

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

import os
import ctypes.wintypes
from configparser import SafeConfigParser

config = SafeConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))
library_path = config.get('RTDMessageQueue', 'library_path')
library_name = config.get('RTDMessageQueue', 'library_name')

rtdDll = ctypes.windll.LoadLibrary(os.path.join(library_path, library_name))


# HRESULT MQOpen(const char *qname, int maxQSize = 5, int maxQMsg = 32);
mq_open = rtdDll.MQOpen
mq_open.restype = ctypes.wintypes.HRESULT
mq_open.argtypes = [ctypes.c_char_p]

#HRESULT MQClose(const char *qname);
mq_close = rtdDll.MQClose
mq_close.restype = ctypes.wintypes.HRESULT
mq_close.argtypes = [ctypes.c_char_p]

#HRESULT MQSend(const char *qname, const char *msg);
mq_send = rtdDll.MQSend
mq_send.restype = ctypes.wintypes.HRESULT
mq_send.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

#HRESULT MQRecv(const char *qname, char **msg);
mq_recv = rtdDll.MQRecv
mq_recv.restype = ctypes.wintypes.HRESULT
mq_recv.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
