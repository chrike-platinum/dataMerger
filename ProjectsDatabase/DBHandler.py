__author__ = 'christiaan'
import cPickle as pickle
from project import Project
import os
databaseFolder="Database/"
script_dir = os.path.dirname(__file__)

def resetProgramSettings():
    dict = {'HTML-output directory':'','PDF-output directory': '', 'Percentage rainy day': 20, 'Percentage cloudy day': 20}
    with open(script_dir+'/'+databaseFolder+"programSettings.dat", "wb") as f:
        pickle.dump(dict, f)

def saveProgramSettings(dict):
    dict = dict
    with open(script_dir+'/'+databaseFolder+"programSettings.dat", "wb") as f:
        pickle.dump(dict, f)

def getAllSettings():
    with open(script_dir+'/'+databaseFolder+"programSettings.dat", "rb") as f:
        settings = pickle.load(f)
    return settings

def updateProgramSettings(newSettings):
    try:
        with open(script_dir+'/'+databaseFolder+"programSettings.dat") as f:
            settings = pickle.load(f)
    except:
        print('Data not found!')
        raise
    for setting in newSettings:
        settings[setting[0]]=setting[1]
    saveProgramSettings(settings)




def resetIDList():
    list=[]
    with open(script_dir+'/'+databaseFolder+"ProjectIDList.dat", "wb") as f:
        pickle.dump(list, f)

def loadIDList():
    try:
        with open(script_dir+'/'+databaseFolder+"ProjectIDList.dat","rb") as f:
            list = pickle.load(f)
    except:
        print('ID list could not be loaded')
        raise
    return list

def updateIDList(ID,projectName):
    try:
        list = loadIDList()
    except:
        print('ID list could not be loaded')
    list.append((ID,projectName))
    with open(script_dir+'/'+databaseFolder+"ProjectIDList.dat", "wb") as f:
        pickle.dump(list,f)

def removeProjectFromIDList(project):
    list = loadIDList()
    list.remove((project.DBID,project.name))
    with open(script_dir+'/'+databaseFolder+"ProjectIDList.dat", "wb") as f:
        pickle.dump(list,f)



def getNextProjectID():
    list = loadIDList()
    if (list ==[]):
        returnValue = 0
    else:
        returnValue = int(list[-1][0])+1
    return returnValue


def loadProject(projectID):
    try:
        with open(script_dir+'/'+databaseFolder+"ProjectDB"+str(projectID)+".dat","rb") as f:
            project = pickle.load(f)
    except:
        print('Project not found!')
        raise
    return project

def saveProject(project):
    projectID=project.DBID
    try:
        file = loadProject(projectID)
        with open(script_dir+'/'+databaseFolder+"projectDB"+str(projectID)+".dat", "wb") as f:
                    pickle.dump(project, f)
        print('Project data updated!')
    except:
        print('Data not found, added new project to database')
        projectID = getNextProjectID()
        project.setDBID(projectID)
        with open(script_dir+'/'+databaseFolder+"projectDB"+str(projectID)+".dat", "wb") as f:
                pickle.dump(project, f)
        updateIDList(projectID,project.name)
        print('Project data saved!')

def deleteProject(project):
    filelist = [ f for f in os.listdir(script_dir+'/'+databaseFolder) if f.endswith(".dat") ]
    for f in filelist:
        print('File',f)
        print('FileName to delete','projectDB'+str(project.DBID)+'.dat')
        if f == 'projectDB'+str(project.DBID)+'.dat':
            os.remove(script_dir+"/"+databaseFolder+"/"+f)
            removeProjectFromIDList(project)


def resetDB():
    filelist = [ f for f in os.listdir(script_dir+'/'+databaseFolder) if f.endswith(".dat") ]
    for f in filelist:
        os.remove(script_dir+"/"+databaseFolder+"/"+f)
    resetIDList()
    resetProgramSettings()

def getAllProjectObjects():
    IDlist = loadIDList()
    projectsList=[]
    for projectTuple in IDlist:
        try:
            projectsList.append(loadProject(projectTuple[0]))
        except:
            print('projectDB file not found but in IDlist')
    return projectsList

def reloadDB():
    resetIDList()
    newID=0
    filelist = [ f for f in os.listdir(script_dir+'/'+databaseFolder) if (f.endswith(".dat") and f.lower().startswith("projectdb"))]
    newIDlist=[]
    for fileName in filelist:
        try:
            with open(script_dir+'/'+databaseFolder+fileName,"rb") as f:
                project = pickle.load(f)
                project.DBID=newID
                saveProject(project)
                newIDlist.append((newID,project.name))
                newID+=1
        except:
            print('Project not found!')
            raise

    with open(script_dir+'/'+databaseFolder+"ProjectIDList.dat", "wb") as f:
        pickle.dump(newIDlist, f)



