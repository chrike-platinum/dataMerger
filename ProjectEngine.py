__author__ = 'christiaan'

from project import Project






def createProject(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData,GHIdf,sampleRate):
    project = Project(generalData,geoData,totalData,inverterData,maintananceData,ExtraData,adresData,GHIdf)
    project.updateInverterData(sampleRate)
    return project

