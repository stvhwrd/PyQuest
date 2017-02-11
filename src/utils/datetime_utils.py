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

from datetime import datetime, date, time
from dateutil.tz import tzlocal
import dateutil.parser

def datetime_now():
    return datetime.now()

def datetime_delta_days(d1, d2):
    delta_days = 0
    if isinstance(d1, datetime) and isinstance(d2, datetime):
        delta = d2 - d1
        delta_days = delta.days
    return delta_days

def get_secs_since_epoch():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.datetime.utcnow()
    delta = now - epoch
    return delta.total_seconds()

def get_datetime_from_secs(seconds):
    return datetime.utcfromtimestamp(seconds)

def iso_today():
    today = date.today()
    return today.isoformat()

def iso_today_starttime():
    today = date.today()
    t = time(0,0,0)
    starttime = datetime.combine(today,t).replace(tzinfo=tzlocal())
    return starttime.isoformat()

def iso_today_endtime():
    today = date.today()
    t = time(23,59,59)
    endtime = datetime.combine(today,t).replace(tzinfo=tzlocal())
    return endtime.isoformat()

def iso_time():
    return time.isoformat()

def iso_now():
    now = datetime.now(tzlocal())
    return now.isoformat()

def iso_to_datetime(iso_str):
    return dateutil.parser.parse(iso_str)

def print_datetime(dt_str):
    return dt_str.strftime("%A %B %d %Y  %I:%M:%S %p %Z")
