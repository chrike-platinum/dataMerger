# -*- coding: utf-8 -*-

__author__ = 'christiaan'
from os import listdir
from os.path import isfile, join
import re
import os
import csv
from cStringIO import StringIO

import pandas as pd


def convertToMin(sampleRate):
    if "Min" in sampleRate:
        return float(sampleRate.split('Min', 1)[0])
    if "T" in sampleRate:
        return float(sampleRate.split('T', 1)[0])
    if "H" in sampleRate:
        return float(sampleRate.split('H', 1)[0]) * 60
    if "D" in sampleRate:
        return float(sampleRate.split('D', 1)[0]) * 24 * 60
    if "W" in sampleRate:
        return float(sampleRate.split('W', 1)[0]) * 168 * 60


def searchStartingRowCSV(dataPath,fileName):
    if (dataPath.strip()[-1] =='/'):
        df = pd.read_csv(StringIO(''.join(l.replace(',', ';') for l in open(dataPath+'/'+fileName))), sep=';', encoding='latin1', parse_dates=False,index_col=0,header=None)
    else:
        df = pd.read_csv(StringIO(''.join(l.replace(',', ';') for l in open(dataPath+'/'+fileName))), sep=';', encoding='latin1', parse_dates=False,index_col=0,header=None)
    df=df.dropna(axis=1,how='all')
    inverterName = None
    if 'filetype' in str(df.index.values[0]).lower():
        inverterName = str(df.index.values[0].split()[1])
    if 'serial' in str(df.index.values[2]).lower():
        inverterName = inverterName+ str(df.index.values[2].split()[1])

    df = df.ix[:,1]
    l=df.index.str.count(':').tolist()
    max1 = max(l)
    beginRow = l.index(max1)-1
    dateIncluded = False
    if (len(df.index.values[beginRow+1]) < 13):
        print('searching for date in file name...')
    else:
        dateIncluded = True
    return beginRow,dateIncluded,inverterName


def importCSVFile(dataPath,fileName,sampleRate2):
    sampleRate = str(sampleRate2)
    start,dateIncluded,inverterName = searchStartingRowCSV(dataPath,fileName)

    df = pd.read_csv(StringIO(''.join(l.replace(',', ';') for l in open(dataPath+'/'+fileName))), sep=';', encoding='latin1', parse_dates=True,index_col=0,skiprows=start)
    df=df.dropna(axis=1,how='all')
    ###Extend short dataframes
    dateDF = str(df.index.values[1])[:10]
    endDateDF = str(df.index.values[-1])[:10]
    if ('.' in str(df.index.values[1])[:10]):
        dateparse = lambda x: pd.datetime.strptime(x, '%d.%m.%Y %H:%M')
        df = pd.read_csv(StringIO(''.join(l.replace(',', ';') for l in open(dataPath+'/'+fileName))), sep=';', encoding='latin1',date_parser=dateparse, parse_dates=True,index_col=0,skiprows=start+1)
        df = df.apply(pd.to_numeric, args=('coerce',)).fillna(0)
        df=df.dropna(axis=1,how='all')
        dateDF = str(df.index.values[1])[:10].replace('.','-')
        endDateDF = str(df.index.values[-1])[:10].replace('.', '-')

    test3 = len([col for col in df.columns if '(wh)' in col.lower()])
    test4 = len([col for col in df.columns if '[wh]' in col.lower()])
    if (test3 + test4 > 0):
        df = (df * 60 / convertToMin(sampleRate)) / 1000
        df = df.add_suffix('[kW]')

    test5 = len([col for col in df.columns if '(kwh)' in col.lower()])
    test6 = len([col for col in df.columns if '[kwh]' in col.lower()])
    if (test5 + test6 > 0):
        df = (df * 60 / convertToMin(sampleRate))


    print(str(fileName)+' busy...')
    if dateIncluded:
        print('Date included')
        ix = pd.DatetimeIndex(start=dateDF + " 00:00:00", end=endDateDF + " 23:45:00", freq=sampleRate)
        df = df.resample(sampleRate).mean().ffill().reindex(ix).fillna(0)
    else:
        try:
            date = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", fileName).group(1)
            print('date found: '+date)
            ix = pd.DatetimeIndex(start=date+" 00:00:00", end=date+" 23:45:00", freq=sampleRate)
            df = df.resample(sampleRate).mean().ffill().set_index(ix).fillna(0)

        except:
            print("No date found in file name!!! Used sampleDate of today ")



    if (len([col for col in df.columns if 'pac' in col.lower()]) >=1):
        spike_cols = [col for col in df.columns if 'pac' in col.lower()]
        df = df[spike_cols]
    if (inverterName != None):
       print('Renaming column')
       df = df.rename(columns = {df.columns[0]:inverterName+' '+df.columns[0]})
    test1=len([col for col in df.columns if '(w)' in col.lower()])
    test2=len([col for col in df.columns if '[w]' in col.lower()])
    if(test1+test2>0):
        df=df/1000
        df = df.add_suffix('[kW]')

    return df

def combineAllData(listOfDataFrames):
    if listOfDataFrames!=[]:
        df = pd.concat(listOfDataFrames)
    else:
        df = pd.DataFrame()
    return df


def importAllFilesFromFolder(mypath,sampleRate):
    listOfFileNames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    listOfFileNames = [x for x in listOfFileNames if not x.startswith('.')]
    list = []
    for file in listOfFileNames:
        list.append(importCSVFile(mypath,file,sampleRate))
    return list

def fetchFilesforProject(folderPath):
    projectName = os.path.basename(os.path.normpath(folderPath))
    listofFolders = [x[0] for x in os.walk(folderPath)]
    if(len(listofFolders)>1):
        listofFolders = listofFolders[1:]


    dataFramelist=[]
    headlist =[]
    for i in listofFolders:
        #foldername = os.path.basename(os.path.normpath(i))
        combinedDf =combineAllData(importAllFilesFromFolder(i))
        combinedDf.index = pd.to_datetime(combinedDf.index)
        dataFramelist.append(combinedDf)

    df = pd.concat(dataFramelist,axis=1,ignore_index=False)
    df.index = pd.to_datetime(df.index)
    result=(projectName, df)

    return result

def fetchFilesforInverter(folderPath,colNr,inverterName,sampleRate):
    listofFolders = [x[0] for x in os.walk(folderPath)]
    if(len(listofFolders)>1):
        listofFolders = listofFolders[1:]


    dataFramelist=[]
    for i in listofFolders:
        #foldername = os.path.basename(os.path.normpath(i))
        combinedDf =combineAllData(importAllFilesFromFolder(i,sampleRate))
        if not combinedDf.empty:
            combinedDf.index = pd.to_datetime(combinedDf.index)
            newdf = combinedDf[combinedDf.columns[colNr]].to_frame()
            newdf.columns = [inverterName]
            newdf.index=pd.to_datetime(combinedDf.index)
            dataFramelist.append(newdf)
        else:
            df = pd.DataFrame()
            dataFramelist.append(df)


    df = pd.concat(dataFramelist,axis=1,ignore_index=False)
    return df





def SelectTimeFrameData(timeseries,beginDate,endDate):
    print("Selecting time period...")
    df = timeseries[beginDate:endDate]
    return df


def getIndexOfFirstOccurance(df,searchString):
    searchCOlumn = df[df.columns[0]]
    return searchCOlumn[searchCOlumn=='Month'].index[0]


def collectSolargisData(filePath):
    endColumn=5
    endRow = 12
    filePath=filePath.decode('utf8')
    df_GHI = pd.read_excel(filePath, sheetname="GHI+Temp")
    skips = getIndexOfFirstOccurance(df_GHI,'Month')
    df_GHI = pd.read_excel(filePath, sheetname="GHI+Temp",skiprows=skips+1)
    df_GHI = df_GHI[df_GHI.columns[0:endColumn]].head(n=endRow)




    df_GII = pd.read_excel(filePath, sheetname="GII")
    skips2=getIndexOfFirstOccurance(df_GII,'Month')
    df_GII = pd.read_excel(filePath, sheetname="GII",skiprows=skips2+1)
    df_GII = df_GII[df_GII.columns[0:endColumn]].head(n=endRow)



    df_PV = pd.read_excel(filePath, sheetname="PV")
    skips3=getIndexOfFirstOccurance(df_PV,'Month')
    df_PV = pd.read_excel(filePath, sheetname="PV",skiprows=skips3+1)
    df_PV = df_PV[df_PV.columns[0:endColumn+1]].head(n=endRow)
    return df_GHI,df_GII,df_PV


def findDatastart(path, keyWord):
    rows = list(csv.reader(open(path, 'r'), delimiter=';'))
    rows = [[x.lower() for x in l] for l in rows]
    indices = [i for i, s in enumerate(rows) if keyWord in s[0]]
    try:
        startRow = indices[0] + 1
    except:
        print('C_error could not find keyword to start in datafile')
        startRow = 0
    return startRow


def loadSolargisRealExcel(path):
    start = findDatastart(path, '#data:')
    df = pd.read_csv(StringIO(''.join(l.replace(',', ';') for l in open(path))), sep=';', encoding='latin1',
                     parse_dates=True, index_col=0, skiprows=start)
    try:
        if ('.' in str(df.index.values[1])):
            dateparse = lambda x: pd.datetime.strptime(x, '%d.%m.%Y')
            df = pd.read_csv(StringIO(''.join(l.replace(',', ';') for l in open(path))), sep=';', encoding='latin1',
                             date_parser=dateparse, parse_dates=True, index_col=0, skiprows=start)

        df.Time = pd.to_timedelta(df.Time + ':00', unit='h')
        df.index = df.index + df.Time
        df = df.drop('Time', axis=1)
        df.index.name = 'timestamp'
        df = df[['GHI']]
    except:
        print("C_Notification: DataFrame seems to be in the unique Solcor format, no extra processing is done.")
    print(df)
    return df

    # print(loadSolargisRealExcel('/Users/christiaan/Desktop/Solcor/outputTést/Nueces Del ChoapaSolargis API Data.csv'))
    # print(loadSolargisRealExcel('/Users/christiaan/Desktop/SolarGIS_hourly_1_Bratislava_Slovakia_20170101_20170131.csv'))


def loadCSVData(path, columnName, sampleRate, delimiter=';'):
    start = findDatastart(path, 'fecha/hora')

    df = pd.read_csv(StringIO(''.join(l.replace('\t', ';') for l in open(path))), sep=';',
                     parse_dates=True, index_col=0, skiprows=start - 1, header=0, decimal=",")


    # if not(isinstance(df.index,pd.DatetimeIndex)):
    if delimiter == 'tab':
        dateparse = lambda x: pd.datetime.strptime(x, '%d-%m-%Y %H:%M')
        df = pd.read_csv(StringIO(''.join(l.replace('\t', ';') for l in open(path))), sep=';', encoding='latin1',
                         date_parser=dateparse, parse_dates=True, index_col=0, skiprows=start - 1, header=0,
                         decimal=",")

    df.columns = [x.lower().replace(' ', '') for x in df.columns]
    df = df[['+p/kw', '-p/kw']]

    df = df.astype(float).fillna(0.0)
    df.sort_index(inplace=True)
    dateDF = str(df.index.values[1])[:10]
    endDateDF = str(df.index.values[-1])[:10]

    ix = pd.DatetimeIndex(start=dateDF + " 00:00:00", end=endDateDF + " 23:45:00", freq=sampleRate)
    df = df.resample(sampleRate).mean().ffill().reindex(ix).fillna(0)

    df = df['+p/kw'] + df['-p/kw']
    df = df.to_frame()
    df.columns = [columnName]

    return df


def fetchFilesforProductionMeter(folderPath, columnName, sampleRate):
    return loadCSVData(folderPath, columnName, sampleRate)

# loadCSVData('/Users/christiaan/Downloads/20170424 Puratos.LP','15Min',delimiter='tab')
# loadCSVData('/Users/christiaan/Downloads/20170720 Econut.LP','15Min')
# loadCSVData('/Users/christiaan/Downloads/Medidor AQ 20170627.LP','15Min')
