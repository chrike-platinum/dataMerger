__author__ = 'christiaan'

from project import Project






def createProject(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData):
    project = Project(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData)
    project.updateInverterData()
    return project

