'''Test Market API

@summary: Unit Test for Market APIs

@see: http://www.questrade.com/api/documentation/getting-started

@copyright: 2017
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

import unittest
from questrade.api import market


class Test(unittest.TestCase):

    def testSymbol(self):
        print "--------------------------"
        print "Testing Market symbol"
        
        r = market.symbol('11419765')  #Symbol Id for GOOG
        self.assertIsNotNone(r, "response not found")
        print r
        
        s = r.get('symbols')
        self.assertIsNotNone(s, "symbol not found")
        
        for i in s:
            sid = i.get('symbolId')
            self.assertEqual(str(sid), '11419765', "symbol Id does not match")


if __name__ == "__main__":
    unittest.main()
    