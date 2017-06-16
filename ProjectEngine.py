# -*- coding: utf-8 -*-
__author__ = 'christiaan'

from project import Project
import dataHandler as DH
import time





def createProject(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData,solargisFileLocation,GHIdf):
    project = Project(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData,solargisFileLocation,GHIdf)
    project.updateInitialInverterData()
    return project



def checkForDataUpdates(project):
    i=0
    for inverter in project.inverters:
        inverter[1].updateNextInverterData(i)
        i+=1


def updateAllProjects():
    projectList = DH.getAllSavedProjects()
    for project in projectList:
        try:
            print('updating: '+str(project.name))
            checkForDataUpdates(project)
            #time.sleep(1)
            DH.saveProject(project)
        except:
            print('Could not update '+str(project.name)+'. 1) Check directory name 2) only .csv production files are allowed in the directory')






