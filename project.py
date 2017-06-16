__author__ = 'christiaan'
import dataLoader as DL
import pandas as pd
import datetime
from datetime import timedelta, date
import CalculationEngine as CE
from inverter import Inverter

class Project(object):



    def __init__(self, generalData,geoData,totalData,inverterData,maintanceData,ExtraData,adresData,solargisFileLocation,GHIdf):
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



        self.inverters =[]
        inverterID=0
        for inverterdat in inverterData:
            type = inverterdat[0]
            kWP=float(inverterdat[1].replace(',','.'))
            kW=float(inverterdat[2].replace(',','.'))
            extra =inverterdat[3]
            filePath=inverterdat[4]
            if (inverterdat[5]!=""):
                columnNumber=int(inverterdat[5])
            else:
                columnNumber=1
            sampleRate = inverterdat[6]
            inverter = Inverter(type,kWP,kW,extra,filePath,columnNumber,[],sampleRate)
            self.inverters.append((inverterID,inverter))
            inverterID+=1

        self.cleaningDates=maintanceData[0]
        if ExtraData ==[]:
            self.commentList = []
        else:
            self.commentList = [ExtraData]

        self.gridProblemData=maintanceData[1]
        self.maintenanceData = maintanceData[2]
        self.internetProblems=maintanceData[3]


        self.GHIdf=GHIdf
        self.DBID=None
        self.solargisFileLocation=solargisFileLocation


    def __getitem__(self, item):
        return getattr(self, item)



    def updateInitialInverterData(self):
        i=0
        listOfDF=[]
        inverterFilePaths = []
        inverterColumnNumbers=[]
        inverterTypes=[]
        for invertertuple in self.inverters:
            inverterFilePaths.append(invertertuple[1].filePath)
            inverterColumnNumbers.append(invertertuple[1].columnNumber)
            inverterTypes.append(invertertuple[1].type)

        for path,col,inverterType in zip(inverterFilePaths,inverterColumnNumbers,inverterTypes):
                inverter = self.getInverter(i)
                inverterData = DL.fetchFilesforInverter(path,col-1,inverterType+'-'+str(i),inverter.sampleRate)
                inverter.updateInitialInverterData(inverterData)
                i+=1

    def updateProjectWithNextInverterData(self):
        for inverter in self.inverters:
            inverter.updateNextInverterData()




    def getAllInverterDatafromTo(self,projectDateBeginString,projectDateEndString):
        listOfDF=[]
        for invertertuple in self.inverters:
            listOfDF.append(invertertuple[1].inverterData)
        df = pd.concat(listOfDF,axis=1,ignore_index=False)
        print('df',projectDateBeginString)
        print('dfPart',df[projectDateBeginString:projectDateEndString])
        return df[projectDateBeginString:projectDateEndString]

    def getAllInverterData(self):
        listOfDF=[]
        for invertertuple in self.inverters:
            listOfDF.append(invertertuple[1].inverterData)
        df = pd.concat(listOfDF,axis=1,ignore_index=False)
        return df


    def getInverter(self,inverterID):
        return self.inverters[inverterID][1]


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

    def getExpectedPR(self,begindateString,enddateString):
        beginDate = datetime.datetime.strptime(begindateString,'%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(enddateString,'%Y-%m-%d %H:%M:%S')
        df = self.GHIdf
        return df[df.columns[5]][beginDate:endDate].mean()

    def removeInverter(self,inverterID,inverter):
        self.inverters.remove((inverterID,inverter))
        i = 0
        newInverterlist=[]
        for tuple in self.inverters:
            newInverterlist.append((i,tuple[1]))
            i+=1
        self.inverters=newInverterlist

    def addInverter(self,inverter):
        newID = self.inverters[-1][0]+1
        self.inverters.append((newID,inverter))
        self.updateInitialInverterData()

    def setDBID(self,ID):
        self.DBID=ID

    def updateSolargisFile(self,solargisFilePath,year):
        self.solargisFileLocation=str(solargisFilePath)
        df=self.GHIdf
        newGHIdf = CE.collectSolarisData(self.solargisFileLocation,year)
        if (not newGHIdf.empty):
            returndf = newGHIdf.merge(df,right_index=True,left_index=True,how='outer',on=list(df))
        else:
            returndf=df
        print('return',returndf)
        self.GHIdf=returndf







