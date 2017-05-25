__author__ = 'christiaan'

from scipy.integrate import simps
import solcorWeatherEngine as SWE
import pandas as pd


def convertToHours(sampleRate):
    if "Min" in sampleRate:
        return float(sampleRate.split('Min', 1)[0])/60
    if "T" in sampleRate:
        return float(sampleRate.split('T', 1)[0])/60
    if "H" in sampleRate:
        return float(sampleRate.split('H', 1)[0])
    if "D" in sampleRate:
        return float(sampleRate.split('D', 1)[0])*24
    if "W" in sampleRate:
        return float(sampleRate.split('W', 1)[0])*168

def calculateTotalAreaVector(DF,sampleRate):
    #Numerical Interation (using simpson's rule)
    list=[]
    for column in DF:
        values = DF[column]
        dx=convertToHours(sampleRate)
        list.append(simps(values, dx=dx))
    return list




def returnAverageRainData(beginDate,endDat,lat,lng):
    df = SWE.requestWeatherData(beginDate,endDat,lat,lng)
    df2 = df[df.columns[2]]
    df2 = df2.replace(-1,0)
    df2.index = pd.to_datetime(df2.index)
    sunUp = '00:00'
    sunDown = '23:45'



    DFList = [group[1] for group in df2.groupby(df2.index.date)]


    resultList = []
    for data in DFList:
        newDf = data.between_time(sunUp,sunDown)
        resultList.append(newDf)


    means = []
    for dataframe in resultList:
        means.append(dataframe.resample('D').sum())
    return pd.concat(means)/24




def getkWhPerDay(dataList):
    dataList[1].index = pd.to_datetime(dataList[1].index)
    DFList = [group[1] for group in dataList[1].groupby(dataList[1].index.day)]

    resultList = []
    dates=[]
    for dat in DFList:
            dates.append(dat.index.values[0])
            dat.index = [pd.Timestamp(d) for d in dat.index]
            freq = pd.infer_freq(dat.index)
            kWh = calculateTotalAreaVector(dat,freq)
            resultList.append(kWh)


    result = resultList#[list(i) for i in zip(*resultList)]

    df = pd.DataFrame(result,index=dates,columns=DFList[0].columns)
    return df

def getTotalkWh(dataList):
    df = getkWhPerDay(dataList)
    sum = df.sum(axis=1)
    totalsum = sum.sum()
    return totalsum



def returnAverageCloudData(beginDate,endDat,lat,lng):
    df = SWE.requestWeatherData(beginDate,endDat,lat,lng)
    df2 = df[df.columns[0]]
    df2 = df2.replace(-1,0)
    df2.index = pd.to_datetime(df2.index)
    sunUp = '7:00'
    sunDown = '19:00'



    DFList = [group[1] for group in df2.groupby(df2.index.date)]


    resultList = []
    for data in DFList:
        newDf = data.between_time(sunUp,sunDown)
        resultList.append(newDf)


    means = []
    for dataframe in resultList:
        means.append(dataframe.resample('D').mean())
    return pd.concat(means)