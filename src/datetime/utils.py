'''datetime utils

@summary: Utility for datetime functions


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

import datetime


def datetime_now():
    return datetime.datetime.now()

def datetime_delta_days(d1, d2):
    delta_days = 0
    if isinstance(d1, datetime) and isinstance(d2, datetime):
        delta = d2 - d1
        delta_days = delta.days
    return delta_days

def get_secs_since_epoch():
    epoch = datetime.datetime.utcfromtimestamp(0)
    now = datetime.datetime.utcnow()
    delta = now - epoch
    return delta.total_seconds()

def get_datetime_from_secs(seconds):
    return datetime.datetime.utcfromtimestamp(seconds)
