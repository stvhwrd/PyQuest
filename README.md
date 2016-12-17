# Questrade API Python Wrapper
A Python wrapper for Questrade's Restful API


<a href="https://questrade.com"><img src="https://pbs.twimg.com/profile_images/3121643627/ab59bf9e1b51307feb88a4f07727eff1_400x400.png" width="75" height="75" /></a>  [![Python](https://www.python.org/static/community_logos/python-logo.png)](https://www.python.org/)



[Questrade](http://www.questrade.com/) is a leading Canadian Discount Brokerage with the goal of allowing investors reach their financial independence.

[Python](https://www.python.org/) is a leading programming language with a rich set of packages to analyze financial data.

This package aims to bridge the gap for developers to create pythonic investing applications with Questrade's Restful API.


### Features
This package currently includes the following features:

 * OAuth 2.0 API requests via HTTPS (TLS)
 * A helper to iniciate the OAuth 2.0 handshaking process with a popup web browser to obtain an access key
 * Optimized calls to request new access tokens via refresh tokens when available
 * Error handling and logging
 * Wrappers for all Questrade Account and Market calls
 * Streaming quotes
 * [xlwings] User Defined Functions (UDFs) that can call all Python wrapped Questrade API's from Microsoft Excel
 * A local SQLite database to minimize API callouts when possible so that rate limits are not hit


### How it works
This package includes the implemention for an AWS https microservice that I host to retrieve an initial access token.  Once an initial access token is obtained, subsequest Questrade API calls can be made.  This microservice is safe to use and will never store any access tokens on any server.  You can manually use this microservice freely to obtain your personalized access token as follows:

 1. Point your web browser to [https://n0mq97v6uj.execute-api.us-east-1.amazonaws.com/dev/authorize](https://n0mq97v6uj.execute-api.us-east-1.amazonaws.com/dev/authorize)
 2. Login with your Questrade credentials
 3. Accept the Authorization Request to receive an access token from Questrade.

The above steps are programmatically followed when leveraging the Python API wrappers in this package.  In addition, when using this framework, new access tokens are automatically obtained after they've expired by using a refresh token when possible.


### Requirements
 - Python 2.7.11 - Note that 2.7 is used because of the extensive financial packages that exist for Python 2.7 as opposed to 3.5
 - Questrade user account


### Operating Systems
This package has been tested to work on Windows 7 or above.  Most of the features will also work on Mac OS X and Linux operating systems but have not been tested.


### Development Setup
Eclipse [PyDev] was used as the primary IDE.

[virtualenv] was also integrated with this project in PyDev.  Once you have Python 2.7 and your virtualenv activated, enter the following command 

`pip install requirements.txt`

This will download and install all the required Python package dependencies that are needed.


### Technologies
Some of the technologies leveraged in this project are the following:

 - Flask
 - AWS Lambda + API Gateway
 - OAuth2
 - Zappa
 - requests
 - WebSockets
 - Selenium
 - Twisted
 - Threading
 - xlwings
 - ctypes
 - SQLite
 - RTD (real-time data for Excel)
 
    Note: An efficient RTD Server was created in another project to integrate real-time data from Python, or any other COM application, into Excel.  You can learn more about this project at [Message Queue RTD Server](https://github.com/pcinat/MessageQueueRTDServer)



### License
Licensed under the Apache License, Version 2.0 (the "License"). You may obtain a copy of the License at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the specific language governing permissions and limitations under the License.


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [xlwings]: <https://www.xlwings.org/>
   [PyDev]: <http://www.pydev.org/>
   [virtualenv]: <http://docs.python-guide.org/en/latest/dev/virtualenvs/>
   
