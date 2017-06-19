__author__ = 'christiaan'
import dataLoader as DL
import pandas as pd
import datetime
from datetime import timedelta, date
import CalculationEngine as CE


class Inverter(object):



    def __init__(self, type,kWP,kw,extra,filePath,columnNumber,inverterData,sampleRate):
        self.type = type
        self.kWP=kWP
        self.kW=kw
        self.extra=extra
        self.sampleRate = sampleRate
        self.filePath = filePath
        self.columnNumber = columnNumber
        self.inverterData=inverterData




    def __getitem__(self, item):
        return getattr(self, item)

    def updateInitialInverterData(self,inverterData):
        self.inverterData = inverterData


    def updateNextInverterData(self,i):
        updatedDF = CE.updateInverterData(self,i)
        self.inverterData=updatedDF

    def getInverterDatafromTo(self,beginDate,endDate):
        return self.inverterData[beginDate:endDate]





