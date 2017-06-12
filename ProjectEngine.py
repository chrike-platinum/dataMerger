__author__ = 'christiaan'

from project import Project






def createProject(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData,solargisFileLocation,GHIdf):
    project = Project(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData,solargisFileLocation,GHIdf)
    project.updateInverterData()
    return project

