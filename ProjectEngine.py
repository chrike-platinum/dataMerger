__author__ = 'christiaan'

from project import Project






def createProject(generalData,totalData,inverterData,cleaningData,ExtraData):
    project = Project(generalData,totalData,inverterData,cleaningData,ExtraData)
    project.updateInverterData()
    return project

