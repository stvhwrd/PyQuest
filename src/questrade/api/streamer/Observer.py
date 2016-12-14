'''Stream Publisher

@summary: An abstract observer in the Publish/Subscriber design pattern.
    Sub-classes should implement the update method for a specific
    purpose.

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

from abc import ABCMeta, abstractmethod
 
class Observer(object):
    __metaclass__ = ABCMeta
 
    @abstractmethod
    def update(self, *args, **kwargs):
        pass
