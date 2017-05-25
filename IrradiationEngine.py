__author__ = 'christiaanleysen'


import Pysolar.solar as PS
import pandas as pd

import datetime
from time import gmtime, strftime
import time
print(time.tzname)




startDate = "2017-05-01 17:00:00.001"
endDate = "2017-05-07 17:00:00.001"

startDate = pd.to_datetime(startDate)
endDate = pd.to_datetime(endDate)




lat = -33.447487
lng = -70.673676


days = [startDate + datetime.timedelta(days=x) for x in range((endDate-startDate).days + 1)]
list=[]
for day in (days):
    print(day)
    altitude_deg = PS.GetAltitude(lat,lng,day)
    radiation = PS.radiation.GetRadiationDirect(day, altitude_deg)
    list.append(radiation)
print(list)