__author__ = 'christiaan'
import dataLoader as DL
import pandas as pd

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
        self.totAvg=float(totalData[2].replace(',','.'))
        self.totExtra=totalData[3]


        self.inverterTypes=[x[0] for x in inverterData]

        self.invertersTotKWP=[float(x[1].replace(',','.')) for x in inverterData]

        self.invertersTotkw=[float(x[2].replace(',','.')) for x in inverterData]
        self.invertersAvg=[float(x[3].replace(',','.')) for x in inverterData]
        self.invertersExtra=[x[4] for x in inverterData]
        self.inverterFilePaths=[x[5] for x in inverterData]
        self.inverterColumnNumbers=[int(x[6]) if x[6]!="" else 1 for x in inverterData]


        self.cleaningDates=maintanceData[0]
        self.commentList = [ExtraData]

        self.gridProblemData=maintanceData[1]
        self.maintenanceData = maintanceData[2]
        self.internetProblems=maintanceData[3]

        self.GHIdf=GHIdf






        self.inverterData=[]

    def __getitem__(self, item):
        return getattr(self, item)

    def updateInverterData(self):
        i=0
        listOfDF=[]
        for path,col,inverterType in zip(self.inverterFilePaths,self.inverterColumnNumbers,self.inverterTypes):
                print('fetch')
                listOfDF.append(DL.fetchFilesforInverter(path,col-1,inverterType))

        i+=1
        self.inverterData = pd.concat(listOfDF,axis=1,ignore_index=False)

    def getInverterDatefromTo(self,beginDate,endDate):
        return self.inverterData[beginDate:endDate]


    def getGHI(self,monthString):
        monthIndex = int(monthString)
        print(monthIndex)
        df = self.GHIdf
        print(df[df.columns[0]])
        return df[df.columns[0]][monthIndex-1]

    def getGII(self,monthString):
        monthIndex = int(monthString)
        print(monthIndex)
        df = self.GHIdf
        return df[df.columns[1]][monthIndex-1]

    def getPercentageChange(self,monthString):
        monthIndex = int(monthString)
        print(monthIndex)
        df = self.GHIdf
        return df[df.columns[2]][monthIndex-1]

    def getDailyAverageKWhKWp(self,monthString):
        monthIndex = int(monthString)
        print(monthIndex)
        df = self.GHIdf
        return df[df.columns[3]][monthIndex-1]

    def getMonthlyAverageKWhKWp(self,monthString):
        monthIndex = int(monthString)
        print(monthIndex)
        df = self.GHIdf
        return df[df.columns[4]][monthIndex-1]



