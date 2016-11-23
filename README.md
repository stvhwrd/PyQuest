# Questrade API Python Wrapper [![Questrade](http://www.questrade.com/Resources/images/global/header/questrade_logo.svg)](http://www.questrade.com/)[![Python](https://www.python.org/static/community_logos/python-logo.png)](https://www.python.org/)
A Python wrapper for the Questrade API

[Questrade](http://www.questrade.com/) is a leading Canadian Discount Brokerage with the goal of allowing investors to reach their financial independence.

[Python](https://www.python.org/) is a leading programming language with a rich set of packages to analyze financial data.

This package aims to bridge the gap for developers so that they can create pythonic investing applications with Questrade's Restful API.


### Features
This package currently includes the following features:
* OAuth 2.0 API requests via HTTPS (TLS)
* A helper to iniciate the OAuth 2.0 handshaking process with a popup web browser
* Optimized calls to request new access tokens via refresh tokens when available
* Error Handling and logging
* Wrappers for all Account and Market calls
* Streaming services
* [xlwings] User Defined Functions (UDFs) that can call all Python wrapped Questrade API's from Microsoft Excel
* A local database to minimize API callouts when possible so that rate limits are not hit


### Requirements
- Python 3 or above
- Questrade user account


### How it works
This package includes the implemention for an AWS https microservice that I host to retrieve an initial access token.  Once an initial access token is obtained, subsequest Questrade API calls can be made.  This microservice is safe to use and will never store any access tokens on any server.  You can manually use this microservice freely to obtain your personalized access token as follows:
 - Point your web browser to  https://n0mq97v6uj.execute-api.us-east-1.amazonaws.com/dev/authorize
 - Login with your Questrade credentials
 - Accept the Authorization Request to receive an access token from Questrade.

The above steps are programmatically followed when leveraging the Python API wrappers in this package.  In addition, when using the framework implemented in this package, new access tokens are automatically obtained after they've expired by using a refresh token when possible.


### Operating Systems
This package has been tested to work on Windows 7 or above.  Most of the features will also work on Mac OS X and Linux operating systems but have not been tested.


### License
Licensed under the Apache License, Version 2.0 (the "License"). You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the specific language governing permissions and limitations under the License.


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [xlwings]: <https://www.xlwings.org/>
   
