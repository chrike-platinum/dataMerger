__author__ = 'christiaan'

from project import Project






def createProject(generalData,totalData,inverterData,cleaningData,ExtraData,adresData):
    project = Project(generalData,totalData,inverterData,cleaningData,ExtraData,adresData)
    project.updateInverterData()
    return project

