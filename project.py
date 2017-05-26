__author__ = 'christiaan'
import dataLoader as DL
import pandas as pd

class Project(object):



    def __init__(self, generalData,totalData,inverterData,cleaningData,ExtraData,adresData):
        self.name = generalData[0]
        self.projectOrientation=generalData[1]
        self.projectInclination=generalData[2]
        self.projectLatitude=generalData[3]
        self.projectLongitude=generalData[4]

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


        self.cleaningDates=cleaningData
        self.commentList = ExtraData

        self.gridProblemData=[]
        self.maintenanceData = []
        self.internetProblems=[]



        self.inverterData=[]

    def __getitem__(self, item):
        return getattr(self, item)

    def updateInverterData(self):
        i=0
        listOfDF=[]
        for path,col,inverterType in zip(self.inverterFilePaths,self.inverterColumnNumbers,self.inverterTypes):
                listOfDF.append(DL.fetchFilesforInverter(path,col-1,inverterType))
        i+=1
        self.inverterData = pd.concat(listOfDF,axis=1,ignore_index=False)


