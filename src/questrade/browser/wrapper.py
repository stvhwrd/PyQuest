'''Helper module to login to Questrade and retrieve an authorization token

@summary: This is a simple module that will launch a Chrome browser and allow the user to
    login with their Questrade credentials and Allow the Authorization Token App
    to return a token.  Once the token is received, it is stored locally so that
    it can be used to make Questrade API calls.

@note: The locally stored token is placed in the user's home directory under filename
    'questrade_token.json'.
    
    Windows:    C:\\Users\\<username>\\questrade_token.json
    OS X:       /Users/<username>/questrade_token.json
    Linux:      /home/<username>/questrade_token.json
@note: This module uses Selenium to automatically launch a browser that allows the user
    to enter their Questrade credentials.  Currently, this helper module only works
    on Windows and launches a Chrome browser.
    
@requires: Chrome browser installed on Windows

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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configparser import SafeConfigParser
import os
import json
import requests
from selenium.common.exceptions import TimeoutException

config = SafeConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))

authorization_url = config.get('Questrade', 'authorization_url')
refresh_url = config.get('Questrade', 'refresh_url')
username = config.get('Questrade', 'username', vars={'username':''})
password = config.get('Questrade', 'password', vars={'password':''})


def login():
    browser = webdriver.Chrome(os.path.join(os.path.abspath(os.path.dirname(__file__)),'chromedriver.exe'))

    token = {}
    browser.get(authorization_url)
    try:
        # Wait on the login Submit button to appear
        WebDriverWait(browser, 30).until(
            EC.visibility_of_element_located((By.ID, 'ctl00_DefaultContent_btnContinue'))
        )
        
        # Find the username and password input fields
        inputElem_username = browser.find_element_by_id('ctl00_DefaultContent_txtUsername')
        inputElem_password = browser.find_element_by_id('ctl00_DefaultContent_txtPassword')
    
        # Populate the username and input fields
        inputElem_username.send_keys(username)
        inputElem_password.send_keys(password)
        
    
        # Wait on the Authorization Allow button to appear
        WebDriverWait(browser, 60).until(
            EC.visibility_of_element_located((By.ID, 'ctl00_DefaultContent_btnAllow'))
        )
    
        # Wait on the Authentication Token JSON to appear
        jsonElement = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, 'pre'))
        )
        
        token = json.loads(jsonElement.text)
        __store_token__(jsonElement.text)
        
        
    except TimeoutException:
        print('Time expired while attempting to login')
        
    finally:
        browser.quit()
        
        return token


def refresh_token(refresh_token):
    params = {'refresh_token': refresh_token}
    r = requests.get(refresh_url, params)
    if r.status_code == requests.codes.ok:
        token = json.loads(r.text)
        __store_token__(r.text)
    else:
        token = None
    
    return token

       
def __store_token__(jsonTxt):
    with open(os.path.join(os.path.expanduser('~'), 'questrade_token.json'), 'w') as f:
            f.write(jsonTxt)


if __name__ == "__main__":
    login()
