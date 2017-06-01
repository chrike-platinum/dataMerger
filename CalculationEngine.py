__author__ = 'christiaan'

from scipy.integrate import simps
import solcorWeatherEngine as SWE
import dataLoader as DL
import pandas as pd
import datetime


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
    DFList = [group[1] for group in dataList[1].groupby(dataList[1].index.date)]

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


def collectSolarisData(path,year):
    df_GHI,df_GII,df_PV = DL.collectSolargisData(path)
    #monthNr = pd.to_datetime(beginDate).month
    df_GHI_column= df_GHI[df_GHI.columns[2]].to_frame()
    df_GII_column =df_GII[df_GII.columns[2]].to_frame()
    df_PV_column1 =df_PV[df_PV.columns[2]].to_frame()
    df_PV_column2 =df_PV[df_PV.columns[1]].to_frame()
    dfPercent_column = (df_GII_column[df_GII_column.columns[0]]/df_GHI_column[df_GHI_column.columns[0]]).to_frame()
    df = pd.concat([df_GHI_column,df_GII_column,dfPercent_column,df_PV_column1,df_PV_column2],axis=1)
    df.columns = [df.columns.values[0]+'_GHI',df.columns.values[1]+'_GII','percentageChange',df.columns.values[3]+' daily',df.columns.values[3]+' monthly']
    monthList = [1,2,3,4,5,6,7,8,9,10,11,12]
    dateList=[]
    #create dates
    for i in monthList:
        dateString = '1'+'-'+str(i)+'-'+str(year)
        date = datetime.datetime.strptime(dateString,'%d-%m-%Y')
        dateList.append(date)


    df = df.set_index([dateList])
    endDate = (dateList[-1] + pd.DateOffset(day=31)).to_datetime()
    dates = pd.date_range(dateList[0], endDate, freq='D')
    df = df.reindex(dates, method='ffill')
    return df


'''
def reindexforYear(df):
    df['month'] = pd.to_datetime(df.index.values, format='%Y-%m')
    df = df.pivot(index='month', columns='Ghd_GHI')

    start_date = df.index.min() - pd.DateOffset(day=1)
    end_date = df.index.max() + pd.DateOffset(day=31)
    dates = pd.date_range(start_date, end_date, freq='D')
    dates.name = 'date'
    df = df.reindex(dates, method='ffill')

    #df = df.stack(['Ghd_GHI','Gid_GII','percentageChange','Esd daily','Esd monthly']])
    df.stack('Ghd_GHI')
    df = df.sortlevel(level=1)
    df = df.reset_index()
    return df
'''


name = 'NDC_PV-8627-1705-1780_-31.783--70.984.xls'
path='/Users/christiaan/Desktop/Solcor/dataMergeWeek/'
print(collectSolarisData(path+name,2017))
#