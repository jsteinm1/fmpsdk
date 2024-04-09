from decouple import config
import fmpsdk
import datetime as dt

apikey = config("FMP_APIKEY")
from_date = "2024-02-15"
to_date = "2024-02-29"

from_date = dt.datetime(2024,1,1)
to_date = dt.datetime(2024,1,15)

earning_calendar = fmpsdk.earning_calendar(apikey, from_date, to_date)

#print(earning_calendar)
print(len(earning_calendar))