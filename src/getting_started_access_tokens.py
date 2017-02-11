'''getting_started_access_tokens

@summary: Helper module to get started with how access tokens work with
    this package

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

from questrade.token import token_ops
from questrade.api import api_utils


if __name__ == '__main__':
    print '''===========================================================================
Welcome to Questrade API - Python Wrapper

This package contains many features to help you create pythonic programs
leveraging Questrade's API to gather data.  You can simply use it to
gather your account balances or stream live data from the markets.

To get started, we walk through a couple checkpoints.  First, you will
need to have a Questrade account already setup with a user id and password.
Second, in order to gain secure access to Questrade's API, you will need
to obtain an access token.

This module focuses on giving you a better understanding of what access
tokens and refresh tokens are and how they are fetched.  In the end you'll
learn that the Questrade API calls made in this package handles it all
for you automatically.

In the getting_started_api_calls.py module, we jump right into making
Questrade API calls.
'''
    raw_input("\nPress enter key to continue... ")
    
    print '''
===========================================================================
Authorization and Access Tokens

We will now attempt to fetch an access token so you can start using
Questrade's API.  The first time an access token is obtained, you will have
to go through the OAuth2 handshaking process as follows:
1) A web browser will launch to the Questrade login page
2) Enter your Questrade id and password
3) Questrade may ask one of your security questions
4) Enter the correct answer to your security question
5) Questrade will ask you to grant authorization for this app to return an
   access token
6) Select Authorize
Note:  Currently, step 1 above only works on Windows systems
'''
    raw_input("\nPress enter key to continue... ")
    
    token = api_utils.get_valid_token()
    if token_ops.is_valid_token(token):
        print '''
Access token obtained and valid!

Your access token has been downloaded to your computer under the following location:
C:\\Users\\<username>\\questrade_token.json
where <username> is the name of the user you are currently logged in as.

Here is what your access token looks like:
'''
        token_ops.print_token(token)
    else:
        print "Could not retrieve a valid access token. Unfortunately, we will have to stop here."
        exit()
    
    raw_input("\nPress enter key to continue... ")
    print'''
Now that we have an access token, we can begin to make use of Questrade's
API.  But first, there is still a little more to learn about access tokens.
Access tokens have an expiry time that is set by the server. Once the expiry
time has been reached, a new access token is needed to continue using the
Questrade API.  If we already have an access token, we can request a
new access token with a refresh token and avoid re-entering a username and
password as long as we make the request within the allowable time period that
Questade allows a refresh token to be made.

We will now attempt to fetch a new access token leveraging the refresh token
we were given.
'''
    raw_input("\nPress enter key to continue... ")
    
    token = token_ops.refresh_token(token['refresh_token'])
    if token_ops.is_valid_token(token):
        print '''
Access token obtained through a refresh token!
Here is what your access token looks like now:
'''
        token_ops.print_token(token)
    else:
        print "Could not retrieve a valid access token. Unfortunately, we will have to stop here."
        exit()
    
    raw_input("\nPress enter key to continue... ")
    print '''
Notice this time we didn't have to re-enter a username and password as we
did when we fetched the original access token.  However, this only works
if we make the request for a refresh token within an allowable time period
that Questrade servers set based on when the original access token was
received.  If a refresh token request is made beyond that time period, then
a new token can only be retrieved by following the original handshaking
process which requires you to re-enter your username and password.

The good news is that all the Questrade API calls made in this package
handle token authorization automatically for you.  That is, if you don't
have an access token, it will launch a web browser for you to enter your
username and password to obtain an initial access token.  If you already
have an access token, it will automatically request a new refresh token
when needed.  And if both the original access token and refresh tokens
have expired, the package will automatically request a new access token
where you have to re-enter your username and password if needed.  You
simply just have to make the desired API call provided for you in this
package and let it automatically handle the authorization access token
for you.
'''
    
    raw_input("\nPress enter key to continue... ")
    print '''
This concludes our getting started module on access tokens.  You can
now move onto the getting_started_api_calls.py module to see how
Questrade API calls are made in this package.
'''
