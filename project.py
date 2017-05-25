__author__ = 'christiaan'
import dataLoader as DL
import pandas as pd

class Project(object):



    def __init__(self, generalData,totalData,inverterData,cleaningData,ExtraData):
        self.name = generalData[0]
        self.projectOrientation=generalData[1]
        self.projectInclination=generalData[2]
        self.projectLatitude=generalData[3]
        self.projectLongitude=generalData[4]

        self.total=totalData[0]
        self.totalkw=totalData[1]
        self.totAvg=totalData[2]
        self.totExtra=totalData[3]

        self.inverterTypes=[x[0] for x in inverterData]
        self.invertersTot=[x[1] for x in inverterData]
        self.invertersTotkw=[x[2] for x in inverterData]
        self.invertersAvg=[x[3] for x in inverterData]
        self.invertersExtra=[x[4] for x in inverterData]
        self.inverterFilePaths=[x[5] for x in inverterData]
        self.inverterColumnNumbers=[int(x[6]) if x[6]!="" else 1 for x in inverterData]


        self.cleaningDates=cleaningData
        self.commentList = ExtraData

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
        return None
