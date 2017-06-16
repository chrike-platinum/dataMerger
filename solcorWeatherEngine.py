# -*- coding: utf-8 -*-
__author__ = 'christiaanleysen'

import forecastio
import datetime
import pandas as pd
import os.path
import time
import pytz


UTCTimeOfset=-3


chileTimeZone = pytz.timezone('Chile/Continental')


api_key = "1a11c955c4f85429032538cd11a02bfa"
lat = -33.447487
lng = -70.673676
#dateRequested = datetime.datetime(2017, 5, 17, 0, 0)

'''
forecast = forecastio.load_forecast(api_key, lat, lng,time=dateRequested)


for hourlyData in forecast.hourly().data:
        print (hourlyData.cloudCover,hourlyData.time)
'''

def requestCloudDataFile(startDate,endDate,lat,lng):
    print('Collecting weather data...')
    print('startDate',startDate)
    print('endDate',endDate)
    startDate = pd.to_datetime(startDate)
    endDate = pd.to_datetime(endDate)
    cachedfile = cached(startDate,endDate,lat,lng)

    fileName = cachedfile
    if cachedfile==None:
        print('Weather data not in cache')
        days = [startDate + datetime.timedelta(days=x) for x in range((endDate-startDate).days + 1)]
        data = []
        for day in days:
            forecast = forecastio.load_forecast(api_key, lat, lng,time=day)
            print('Collecting weather data of '+str(day))
            #print('sunRise',forecast.daily().data[0].sunriseTime+ datetime.timedelta(hours=UTCTimeOfset))
            #print('sunSet',forecast.daily().data[0].sunsetTime+ datetime.timedelta(hours=UTCTimeOfset))
            generalCloudIndex=-1
            try:
                generalCloudIndex=forecast.daily().data[0].cloudCover
            except:
                pass
            for weatherData in forecast.hourly().data:
                cloudcover=-1
                weatherSummary = -1
                precipIntensitivity = -1
                precipProb=-1
                temp = -1
                visibility = -1
                try:
                    cloudcover=weatherData.cloudCover
                except:
                    pass
                try:
                    weatherSummary= weatherData.summary
                except:
                    pass
                try:
                    precipIntensitivity=weatherData.precipIntensity
                except:
                    pass
                try:
                    precipProb = weatherData.precipProbability
                except:
                    pass
                try:
                    temp = weatherData.temperature
                except:
                    pass
                try:
                    visibility=weatherData.visibility
                except:
                    pass

                data.append((pd.to_datetime(weatherData.time + datetime.timedelta(hours=UTCTimeOfset)),cloudcover,weatherSummary,precipIntensitivity,precipProb,visibility,temp,generalCloudIndex))



        df = pd.DataFrame(list(data),columns=['time','cloudIndex','summary','precipIntensity','precipProb','visibility','temp','generalCloudIndex'])
        df = df.set_index('time')
        startDateString= str(startDate).replace(':',';')
        endDateString=str(endDate).replace(':',';')
        fileName=startDateString+' '+endDateString+' '+str(lat)+str(lng)
        print('Saving weather data...')
        df.to_csv('weatherDataCache/'+fileName, sep='\t',)
        print('Weather data collected!')
    return fileName



def cached(startDate,endDate,lat,lng):
    startDateString= str(startDate).replace(':',';')
    endDateString=str(endDate).replace(':',';')
    fName=startDateString+' '+endDateString+' '+str(lat)+str(lng)


    if os.path.isfile(fName):
        print('Is in file')
        return fName

    fileList = os.listdir("weatherDataCache/")
    possibleFiles = []
    for file in fileList:
        if str(lat)+str(lng) in file:
            possibleFiles.append(file)


    endList=[]
    for posFile in possibleFiles:
        startDateFile = pd.to_datetime(posFile.split(' ')[0]+' '+posFile.split(' ')[1].replace(';',':'))
        endDateFile = pd.to_datetime(posFile.split(' ')[2]+' '+posFile.split(' ')[3].replace(';',':'))
        startDate=pd.to_datetime(startDate)
        endDate=pd.to_datetime(endDate)


        if (startDateFile <= startDate) and (endDateFile >= endDate):
            endList.append(posFile)

    if endList==[]:
        return None
    else:
        file = endList[0]
        return file

def requestWeatherData(startDate,endDate,lat,lng):
    fileName = requestCloudDataFile(startDate,endDate,lat,lng)
    dataframe = pd.read_csv('weatherDataCache/'+fileName,sep='\t',index_col='time')
    dataframe = dataframe[startDate:endDate]
    return dataframe


#d1 = "2017-05-29 00:00:00"
#d2 = "2017-05-30 00:00:00"
#print(requestCloudData(d1,d2,-33.447487,-70.673676))

'''
        "time": 255589200,
        "summary": "Mostly Cloudy",
        "icon": "partly-cloudy-night",
        "precipIntensity": 0,
        "precipProbability": 0,
        "temperature": 23.47,
        "apparentTemperature": 17.05,
        "dewPoint": 16.42,
        "humidity": 0.74,
        "windSpeed": 5,
        "windBearing": 350,
        "visibility": 9.6,
        "cloudCover": 0.78,
        "pressure": 1026.79
'''