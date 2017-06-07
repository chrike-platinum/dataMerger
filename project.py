__author__ = 'christiaan'
import dataLoader as DL
import pandas as pd
import datetime
from datetime import timedelta, date
import CalculationEngine as CE

class Project(object):



    def __init__(self, generalData,geoData,totalData,inverterData,maintanceData,ExtraData,adresData,GHIdf):
        self.name = generalData[0]
        self.projectOrientation=generalData[1]
        self.projectInclination=generalData[2]
        self.structureType=generalData[3]

        self.projectLatitude = geoData[0]
        self.projectLongitude = geoData[1]
        self.projectLatitudeString = geoData[2]
        self.projectLongitudeString = geoData[3]

        self.contactPerson = adresData[0]
        self.street = adresData[1]
        self.city = adresData[2]
        self.telephoneNumber = adresData[3]


        self.totalkWP=float(totalData[0].replace(',','.'))
        self.totalkw=float(totalData[1].replace(',','.'))
        #self.totAvg=float(totalData[2].replace(',','.'))
        self.totExtra=totalData[2]


        self.inverterTypes=[x[0] for x in inverterData]

        self.invertersTotKWP=[float(x[1].replace(',','.')) for x in inverterData]

        self.invertersTotkw=[float(x[2].replace(',','.')) for x in inverterData]
        self.invertersExtra=[x[3] for x in inverterData]
        self.inverterFilePaths=[x[4] for x in inverterData]
        self.inverterColumnNumbers=[int(x[5]) if x[5]!="" else 1 for x in inverterData]


        self.cleaningDates=maintanceData[0]
        self.commentList = [ExtraData]

        self.gridProblemData=maintanceData[1]
        self.maintenanceData = maintanceData[2]
        self.internetProblems=maintanceData[3]

        self.GHIdf=GHIdf






        self.inverterData=[]

    def __getitem__(self, item):
        return getattr(self, item)

    def updateInverterData(self,sampleRate):
        i=0
        listOfDF=[]
        for path,col,inverterType in zip(self.inverterFilePaths,self.inverterColumnNumbers,self.inverterTypes):
                listOfDF.append(DL.fetchFilesforInverter(path,col-1,inverterType+'-'+str(i),sampleRate))
                i+=1
        self.inverterData = pd.concat(listOfDF,axis=1,ignore_index=False)



    def getInverterDatafromTo(self,beginDate,endDate):
        return self.inverterData[beginDate:endDate]


    def getGHI(self,begindateString,enddateString):
        beginDate = datetime.datetime.strptime(begindateString,'%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(enddateString,'%Y-%m-%d %H:%M:%S')
        df = self.GHIdf
        return df[df.columns[0]][beginDate:endDate].mean()

    def getGII(self,begindateString,enddateString):
        beginDate = datetime.datetime.strptime(begindateString,'%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(enddateString,'%Y-%m-%d %H:%M:%S')
        df = self.GHIdf
        return df[df.columns[1]][beginDate:endDate].mean()

    def getPercentageChange(self,begindateString,enddateString):
        beginDate = datetime.datetime.strptime(begindateString,'%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(enddateString,'%Y-%m-%d %H:%M:%S')
        df = self.GHIdf
        return df[df.columns[2]][beginDate:endDate].mean()
    '''
    def getDailyAverageKWhKWp(self,begindateString,enddateString):
        beginDate = datetime.datetime.strptime(begindateString,'%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(enddateString,'%Y-%m-%d %H:%M:%S')
        df = self.GHIdf
        return df[df.columns[3]][beginDate:endDate].mean()
    '''
    '''
    def getMonthlyAverageKWhKWp(self,begindateString,enddateString):
        beginDate = datetime.datetime.strptime(begindateString,'%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(enddateString,'%Y-%m-%d %H:%M:%S')
        df = self.GHIdf
        return df[df.columns[4]][beginDate:endDate].mean()
    '''
    def getExpectedPR(self,begindateString,enddateString):
        beginDate = datetime.datetime.strptime(begindateString,'%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(enddateString,'%Y-%m-%d %H:%M:%S')
        df = self.GHIdf
        return df[df.columns[5]][beginDate:endDate].mean()




'''

def getDatesBetween(date1, date2):
    datelist=[]
    for n in range(int ((date2 - date1).days)+1):
        datelist.append(date1 + timedelta(n))
    return datelist



def getMonthDistributions(date1, date2):
    dateList = getDatesBetween(date1, date2)
    monthNumberList=[]
    for date in dateList:
        monthNumberList.append(date.month)
    occurences = [(x,monthNumberList.count(x)) for x in set(monthNumberList)]
    return occurences

start_dt = '2017-04-01 00:00:00'
end_dt = '2017-05-30 23:45:00'

'''

