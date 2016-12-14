'''Stream Publisher

@summary: A Publisher in the Publish/Subscriber design pattern.  This
    publisher is aware of all instances created and calls update_observers
    on each StreamPublisher.

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

import weakref

class StreamPublisher(object):
    
    _instances = set()
 
    def __init__(self):
        self.observers = []
        self._instances.add(weakref.ref(self))
 
    def register(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
 
    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
 
    def unregister_all(self):
        if self.observers:
            del self.observers[:]
 
    def update_observers(self, payload, isBinary):
        for observer in self.observers:
            observer.update(payload, isBinary)
    
    @staticmethod
    def onMessage(payload, isBinary):
        for i in StreamPublisher.get_instances():
            StreamPublisher.update_observers(i, payload, isBinary)
        
    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead
