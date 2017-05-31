__author__ = 'christiaan'

from project import Project






def createProject(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData,GHIdf):
    project = Project(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData,GHIdf)
    project.updateInverterData()
    return project

