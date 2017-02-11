'''getting_started_api_calls

@summary: Helper module to get started with how Questrade API calls
    are made withthis package

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

from questrade.api import account
from utils import datetime_utils


if __name__ == '__main__':
    print '''===========================================================================
Welcome to Questrade API - Python Wrapper

This package contains many features to help you create pythonic programs
leveraging Questrade's API to gather data.  You can simply use it to
gather your account balances or stream live data from the markets.

This module focuses on giving you a better understanding of how the
Questrade API calls can be made.  You'll appreciate that all API
calls will automatically handle authorization access tokens for you
so that you can concentrate on just making the appropriate API calls.

If you'd like to better understand how access tokens are fetched, the
getting_started_access_tokens.py module provides a good explanation.
'''
    raw_input("\nPress enter key to continue... ")
    
    print '''
===========================================================================
Questrade API calls

Now let's focus on how Questrade APIs can be called.  First let's begin
with a call to retrieve the Questrade server time.  To do so we make
the following call:
\taccount.time()
Note: If you don't already have an access token, the above all will
automatically call the right procedure to get one for you.
'''
    raw_input("\Press enter key to continue... ")
    r = account.time()
    print "Questrade API responded with JSON:\n%s\n" % r
    t = r.get('time','unknown')
    print "The date time is: %s" % datetime_utils.print_datetime(datetime_utils.iso_to_datetime(t))
    
    print '''
Next let's list the types of accounts you have with Questrade.  To do so
we make the following call:
\taccount.accounts()
'''
    raw_input("\Press enter key to continue... ")
    
    r = account.accounts()
    print "Questrade API responded with JSON:\n%s\n" % r
    print "Your User Id is: %s" % r.get('userId','unknown')
    print "Your Account Numbers and Types are as follows:"
    accs = r.get('accounts',[])
    for a in accs:
        n = a.get('number','unknown')
        t = a.get('type','unknown')
        print "\t%s %s" % (n, t)
        

    print '''
This concludes our getting started module on Questrade API calls. Now that
you have a basic understanding of how you can make Questreade API calls,
you can explore many of the other features this package provides.
'''
