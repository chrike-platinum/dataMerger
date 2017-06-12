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

    def updateInverterData(self,inverterData):
        self.inverterData = inverterData
        #TODO add new data to old data

    def getInverterDatafromTo(self,beginDate,endDate):
        return self.inverterData[beginDate:endDate]





