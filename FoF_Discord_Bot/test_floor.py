import pytz
from datetime import datetime

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

datetime_object = datetime.strptime(datetime_string_test, fmt_datetime_12)

print(datetime_object)
