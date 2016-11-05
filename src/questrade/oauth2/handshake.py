'''Questrade Oauth2 Authorization App

@summary: A micro-service that performs the Oauth2 handshake with Questrade.
    This module is designed to run as a Python Flask Server and is expected
    to run on a secure host (https://).
    
    Once the Flask Server is online, simply goto https://<hostname>/authorize
    This will begin the Oauth2 handshake process. The user will then be
    redirected to Questrade login and authorization screen.  If the user
    accepts the authorization, this service will then go on to return the
    authorization token as a RESTful API in json format.
    
    A refresh token request can also be made with this server as follows
    https://<hostname>/refresh?refresh_token=<refresh_token>

@requires: Requires the Questrade API APP to be configured to allow the callback
    URI from this Flask hostname in addition to getting a Client Id to work with
    @see http://www.questrade.com/api/documentation/getting-started

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

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import uuid
import ConfigParser
import os


__no_session_token__ = {}


config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))

client_id = config.get('Questrade', 'client_id')
client_secret = config.get('Questrade', 'client_secret')
authorization_url = config.get('Questrade', 'authorization_url')
token_url = config.get('Questrade', 'token_url')
api_version = config.get('Questrade', 'api_version')


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.route("/")
def index():
    html = '<html><body><h4>Questrade Oauth2 Service</h4><p><a href="%s">Authorize</a></p></body></html>'
    return html % url_for('.authorize'), 200


@app.route("/authorize")
def authorize():
    questradeAPI = OAuth2Session(client_id, redirect_uri=__get_redirect_uri__(request.url_root))
    user_authorization_url, state = questradeAPI.authorization_url(authorization_url)
    
    session['oauth_state'] = state
    return redirect(user_authorization_url)


@app.route("/callback", methods=["GET"])
def callback():
    questradeAPI = OAuth2Session(client_id, redirect_uri=__get_redirect_uri__(request.url_root), state=session['oauth_state'])
    token = questradeAPI.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    
    __set_session_token__(token)
    
    return redirect(url_for('.token'))


@app.route("/token", methods=["GET"])
def token():
    token = __get_session_token__()
    return jsonify(token), 200


@app.route("/refresh", methods=["GET"])
def refresh():
    token = __get_session_token__()
    refresh_token_arg = request.args.get('refresh_token')
    
    if refresh_token_arg != None:
        refresh_token = refresh_token_arg
    else:
        try:
            refresh_token = token['refresh_token']
        except KeyError:
            refresh_token = ''
        
    questradeAPI = OAuth2Session(client_id, token=token)
    token = questradeAPI.refresh_token(token_url, refresh_token=refresh_token)
    
    __set_session_token__(token)
    
    return redirect(url_for('.token'))


@app.route("/token/<url>", methods=["GET"])
def token_api(url):
    token = __get_session_token__()
    return jsonify(token[url]), 200


@app.route("/questrade/<url>", methods=["GET"])
def questrade_api(url):
    token = __get_session_token__()
        
    questradeAPI = OAuth2Session(client_id, token=token)
    r = questradeAPI.get(__get_base_api_url__() + url)
    
    return jsonify(r.json()), r.status_code


def __get_base_api_url__():
    token = __get_session_token__()
    api_server = token['api_server']
    base_url = api_server + api_version
    return base_url


def __get_redirect_uri__(root_uri):
    return root_uri + 'callback'


def __set_session_token__(token):
    session['oauth_token'] = token


def __get_session_token__():
    return session.get('oauth_token', __no_session_token__)



if __name__ == "__main__":
    app.run(debug=True)
