import pytz
from datetime import datetime
from dateutil.parser import parse
import maya

# for tz in pytz.common_timezones:
#     print(tz)

fmt_datetime_24 = '%Y-%m-%d %H:%M'
fmt_time_24 = '%H:%M'
fmt_datetime_12 = '%Y-%m-%d %I:%M %p'
fmt_time_12 = '%I:%M %p'

# datetime_string_test = '09:26'
# datetime_string_test = '2021-01-06 9:26'
# datetime_string_test = '09:26 pm'
# datetime_string_test = '21-01-06 9:26 pm'
# date_array = [
#     '09:26',
#     '2021-01-06 9:26',
#     '09:26 pm',
#     '06-01-21 9:26 pm',
#     'jan 06 2021 9:26',
#     # '09:26 pst'
# ]

local = pytz.timezone('US/Pacific')
eastern = pytz.timezone('US/Eastern')


# for date in date_array:
#     print('Parsing: ' + date)
#     dt = parse(date)
#     print(dt)
#     print(dt.tzinfo)
#     print('To UTC')
#     local_dt = local.localize(dt)
#     print(local_dt)
#     utc_dt = local_dt.astimezone(pytz.utc)
#     print(utc_dt)
#     est_dt = utc_dt.astimezone(eastern)
#     print(est_dt.time())
#     print('\n')


# datetime_object = datetime.strptime(datetime_string_test, fmt_datetime_12)
# print(datetime_object)

print('*test*')
