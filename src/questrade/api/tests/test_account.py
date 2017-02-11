'''Test Account API

@summary: Unit Test for Account APIs

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
from questrade.api import account


class Test(unittest.TestCase):

    def testTime(self):
        print "--------------------------"
        print "Testing Accounts time"
        
        r = account.time()
        self.assertIsNotNone(r, "response not found")
        print r
        
        t = r.get('time')
        self.assertIsNotNone(t, "time not found")
        print t
        
    def testAccounts(self):
        print "--------------------------"
        print "Testing Accounts accounts"
        
        r = account.accounts()
        self.assertIsNotNone(r, "response not found")
        print r
        
        a = r.get('accounts')
        self.assertIsNotNone(a, "accounts not found")
        print a
        
    def testPositions(self):
        print "--------------------------"
        print "Testing Accounts positions"
        
        r = account.accounts()
        a = r.get('accounts')
        
        for i in a:
            id_ = i.get('number')
            self.assertIsNotNone(id_, "Account id not found")
            
            r = account.accounts_positions(id_)
            self.assertIsNotNone(r, "response not found")
            print r
            
            p = r.get('positions')
            self.assertIsNotNone(p, "positions not found")
            print p
            
    def testBalances(self):
        print "--------------------------"
        print "Testing Accounts balances"
        
        r = account.accounts()
        a = r.get('accounts')
        
        for i in a:
            id_ = i.get('number')
            self.assertIsNotNone(id_, "Account id not found")
            
            r = account.accounts_balances(id_)
            self.assertIsNotNone(r, "response not found")
            print r
            
            b = r.get('perCurrencyBalances')
            self.assertIsNotNone(b, "perCurrencyBalances not found")
            print b
            
    def testExecutions(self):
        print "--------------------------"
        print "Testing Accounts executions"
        
        r = account.accounts()
        a = r.get('accounts')
        
        for i in a:
            id_ = i.get('number')
            self.assertIsNotNone(id_, "Account id not found")
            
            r = account.accounts_executions(id_)
            self.assertIsNotNone(r, "response not found")
            print r
            
            e = r.get('executions')
            self.assertIsNotNone(e, "executions not found")
            print e
            
    def testOrders(self):
        print "--------------------------"
        print "Testing Accounts orders"
        
        r = account.accounts()
        a = r.get('accounts')
        
        for i in a:
            id_ = i.get('number')
            self.assertIsNotNone(id_, "Account id not found")
            
            r = account.accounts_orders(id_)
            self.assertIsNotNone(r, "response not found")
            print r
            
            o = r.get('orders')
            self.assertIsNotNone(o, "orders not found")
            print o
            
    def testActivities(self):
        print "--------------------------"
        print "Testing Accounts activities"
        
        r = account.accounts()
        a = r.get('accounts')
        
        for i in a:
            id_ = i.get('number')
            self.assertIsNotNone(id_, "Account id not found")
            
            r = account.accounts_orders(id_)
            self.assertIsNotNone(r, "response not found")
            print r
            
            ac = r.get('orders')
            self.assertIsNotNone(ac, "activities not found")
            print ac


if __name__ == "__main__":
    unittest.main()
    