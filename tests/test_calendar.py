from decouple import config
import fmpsdk

apikey = config("FMP_APIKEY")
from_date = "2023-02-15"
to_date = "2024-02-29"

earning_calendar = fmpsdk.earning_calendar(apikey)

#print(earning_calendar)
print(len(earning_calendar))