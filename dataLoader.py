__author__ = 'christiaan'
import pandas as pd
from os import listdir
from os.path import isfile, join
import re
import matplotlib.pyplot as plt
import os
import glob

DirPath= '/Users/christiaan/Desktop/Solcor/dataMergeProject/'

DirPath2= '/Users/christiaan/Desktop/Solcor/dataMergeProject/Puratos/'



def searchStartingRowCSV(dataPath,fileName):
    if (dataPath.strip()[-1] =='/'):
        df = pd.read_csv(dataPath+fileName, sep=';', encoding='latin1', parse_dates=False,index_col=0,header=None)
    else:
        df = pd.read_csv(dataPath+'/'+fileName, sep=';', encoding='latin1', parse_dates=False,index_col=0,header=None)
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
    print('beginRow',beginRow)
    dateIncluded = False
    if (len(df.index.values[beginRow+1]) < 13):
        print('searching for date in file name...')
    else:
        dateIncluded = True
    return beginRow,dateIncluded,inverterName

def importCSVFile(dataPath,fileName,sampleRate2):
    sampleRate = str(sampleRate2)
    start,dateIncluded,inverterName = searchStartingRowCSV(dataPath,fileName)

    df = pd.read_csv(dataPath+'/'+fileName, sep=';', encoding='latin1', parse_dates=True,index_col=0,skiprows=start)
    df=df.dropna(axis=1,how='all')
    ###Extend short dataframes
    dateDF = str(df.index.values[0])[:10]
    print(str(fileName)+' busy...')
    if dateIncluded:
        ix = pd.DatetimeIndex(start=dateDF+" 00:00:00", end=dateDF+" 23:45:00", freq=sampleRate)
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
    df = pd.concat(listOfDataFrames)
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

    print(listofFolders)
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
        combinedDf.index = pd.to_datetime(combinedDf.index)
        newdf = combinedDf[combinedDf.columns[colNr]].to_frame()
        newdf.columns = [inverterName]
        newdf.index=pd.to_datetime(combinedDf.index)
        dataFramelist.append(newdf)




    df = pd.concat(dataFramelist,axis=1,ignore_index=False)
    #df.index = pd.to_datetime(df.index)
    result = df
    return df




dataFileName1 = 'Ingeteam 33TL Puratos Inv 1.csv'
dataFileName2 = 'Ingeteam 33TL Puratos Inv 2.csv'
dataFileName3 = 'Ingeteam 33TLM Puratos Inv 3.csv'
dataFileName4 = 'SMA 25000TL30 Gabriel Varela.csv'
dataFileName5 = 'SMA 25000TL30-20000TL30 NDC.csv'
datFileDate = '16-02-2014 jlasdkljlsj.csv'
dataFileName10 = 'Inverter_Day_2017-05-01.csv'
newPath = '/Users/christiaan/Desktop/Solcor/dataMergeWeek/Nueces del Choapa'
newPath2 = '/Users/christiaan/Desktop/Solcor/dataMergeWeek/gabriel Varela'
newPath3 = '/Users/christiaan/Desktop/Solcor/dataMergeWeek/Puratos'
dataFileName11='170503_003.csv'




#print(importCSVFile(newPath,dataFileName10))
#df=combineAllData(importAllFilesFromFolder(newPath))
#print(df)
#print(fetchFilesforProject(newPath3))
#plt.plot(df)
#plt.show()



def SelectTimeFrameData(timeseries,beginDate,endDate):
    print("Selecting time period...")
    df = timeseries[beginDate:endDate]
    #mask = is_leap_and_29Feb(df)
    #f = df.loc[~mask]
    return df


def getIndexOfFirstOccurance(df,searchString):
    searchCOlumn = df[df.columns[0]]
    return searchCOlumn[searchCOlumn=='Month'].index[0]


def collectSolargisData(filePath):
    endColumn=5
    endRow = 12
    df_GHI = pd.read_excel(filePath, sheetname="GHI+Temp")
    skips = getIndexOfFirstOccurance(df_GHI,'Month')
    df_GHI = pd.read_excel(filePath, sheetname="GHI+Temp",skiprows=skips+1)
    #df_GHIYear = df_GHI[df_GHI.columns[2]][endRow]
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

name = 'NDC_PV-8627-1705-1780_-31.783--70.984.xls'
path='/Users/christiaan/Desktop/Solcor/dataMergeWeek/'

collectSolargisData(path+name)
