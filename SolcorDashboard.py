__author__ = 'christiaan'

from bokeh.client import push_session
from random import random
from bokeh.layouts import widgetbox, row, column, layout
from bokeh.models.widgets import CheckboxGroup
from bokeh.models import Button, HoverTool
from bokeh.plotting import figure, curdoc
from bokeh.io import curstate
from bokeh.charts import Line
import bokeh.io as ioa
import dataLoader as DL
from bokeh.models import ColumnDataSource, Range1d, Plot, LinearAxis, Grid, VBox
from bokeh.models.widgets import Panel, Tabs, Paragraph, Div
import CalculationEngine as CE
import matplotlib.pyplot as plt
from bokeh.models import CustomJS
import numpy as np
from bokeh.plotting import Figure
from math import pi
from bokeh.models import DatetimeTickFormatter
import pandas as pd
from bokeh.charts import Bar
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from itertools import cycle
from bokeh.models import LinearAxis, Range1d
from bokeh.models.widgets import PreText
from bokeh.models.tickers import DatetimeTicker
from bokeh.client import push_session
from functools import partial
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown
from bokeh.models import DatePicker, HBox
import datetime
from bokeh.models.widgets import TextInput
import ProjectEngine as PE
from bokeh.models.glyphs import Image
from bokeh.charts import Horizon
import math



#curdoc=curdoc()
projects=[]
currentLayout=None
globNewLayout=None
ProjectName=None

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

cloudyDaythresholdPercentage = 0.2
rainyDaythresholdPercentage = 0.1

#banner = figure(x_range=(0,1), y_range=(0,1))

source = ColumnDataSource(dict(url = ['SolcorBanner2.png']))
xdr = Range1d(start=0, end=1)
ydr = Range1d(start=0, end=1)


#plot = Plot(title="ImageURL", x_range=xdr, y_range=ydr)
#banner = ImageURL(url='SolcorBanner2.png', x=0, y=1, w=1, h=1, anchor="center", global_alpha=0.2)
#plot.add_glyph(source, banner)







def createPlots(datalists,cloudsPerDay,magnification,kWhPerDay,totalkWh,rainPerDay):
####TOTAL
    page=[]
    for project in datalists:
        #p1 = Line(i[1],title=i[0],ylabel= 'kW',xlabel='Time',plot_width=600, plot_height=300)

        p = figure(width=800, height=500,title=project[0],x_axis_type='datetime')
        p.title.text_font_size='15pt'
        p.y_range=Range1d(0, 20)
        p.extra_y_ranges = {"foo": Range1d(start=0, end=200)}
        p.add_layout(LinearAxis(y_range_name="foo"), 'right')

#####ADDkWHDATA
        TotalkWhText = Div(text="""<p style="font-size:20px"> Total: """+str(int(round(totalkWh)))+""" kWh.""",
        width=300, height=30)

        TotalkWhText2 = Div(text="""<p style="font-size:20px"> Avg/day: """+str(int(round(totalkWh/len(kWhPerDay.index.values))))+""" kWh.""",
        width=300, height=30)

        totalKWhPerday = kWhPerDay.sum(axis=1)
        totalKWhPerday.index = totalKWhPerday.index + pd.DateOffset(hours=12)
        kWh =p.line(x=totalKWhPerday.index.values,y=totalKWhPerday,color='red',y_range_name="foo")


#####ADDCloudDATA
        amountOfCloudDays = len([x for x in cloudsPerDay if x >= cloudyDaythresholdPercentage])

        amountOfCloudyDaysTxt = Div(text="""<p style="font-size:20px"> Cloudy days: """+str(amountOfCloudDays),
        width=300, height=30)

        cloudsPerDay.index = cloudsPerDay.index + pd.DateOffset(hours=12)

        l0 = p.circle(x=cloudsPerDay.index.values, y=cloudsPerDay*magnification, line_width=10,color='grey')
        meansLabel = [str(int(round(100*(x),0)))+'%' for x in cloudsPerDay.values.tolist()]

        source = ColumnDataSource(data=dict(x=cloudsPerDay.index,
                                    y=cloudsPerDay*0,
                                    names=meansLabel))


        labels = LabelSet(x='x', y='y', text='names', level='glyph',x_offset=-5, y_offset=5,source=source, render_mode='canvas',text_font_size="10pt")
#######RAINDATA

        amountOfRainDays = len([x for x in rainPerDay if x >= rainyDaythresholdPercentage])

        amountOfRainyDaysTxt = Div(text="""<p style="font-size:20px"> Rainy days: """+str(amountOfRainDays),
        width=300, height=30)




########ADDKW Data
        ##plot
        a=0
        lst = ['green', 'blue','orange','grey']
        colorPool = cycle(lst)
        for b in project[1].columns:
            x= project[1].index.to_datetime()
            print(x[0].day)
            project[1]['dates'] = project[1].index.to_datetime()
            p.line(x=x,y=project[1][project[1].columns[a]],legend=project[1].columns[a],color=next(colorPool))
            a+=1
        p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
            )



        #p.xaxis.major_label_orientation = pi/4
        p.add_layout(labels)
        p.legend.location = "top_right"





        checkbox = CheckboxGroup(labels=["Clouds", "kWh"],
                                 active=[0,1], width=100)
        checkbox.callback = CustomJS(args=dict(line0=l0,line2=labels, line1=kWh), code="""
            //console.log(cb_obj.active);
            line0.visible = false;
            line1.visible = false;
            line2.visible=false;
            for (i in cb_obj.active) {
                //console.log(cb_obj.active[i]);
                if (cb_obj.active[i] == 0) {
                    line0.visible = true;
                    line2.visible = true;
                } else if (cb_obj.active[i] == 1) {
                    line1.visible = true;
                }
            }
            """)







        sidePanel = widgetbox([TotalkWhText,TotalkWhText2,amountOfCloudyDaysTxt,amountOfRainyDaysTxt],height=1000)

        #sidePanel = [checkbox_group,sidePanel]



        list=[]
        list.append([p,checkbox,sidePanel])

        div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)

        dividerWidget = widgetbox(div)

        list.append([dividerWidget])

        tab = Panel(child=layout(list),title='Total')
        tabs = Tabs(tabs=[tab])
        page.append(tabs)
    print('page',page)
    return page



'''
newPath = '/Users/christiaan/Desktop/Solcor/dataMergeWeek/Nueces del Choapa'
newPath2 = '/Users/christiaan/Desktop/Solcor/dataMergeWeek/gabriel Varela'
newPath3 = '/Users/christiaan/Desktop/Solcor/dataMergeWeek/Puratos'
newPath4 = '/Users/christiaan/Desktop/Solcor/dataMergeWeek/Puratos2/Puratos'
newPath5 = '/Users/christiaan/Desktop/Solcor/dataMergeWeek/Neuces2/Nueces'
newPath6 = '/Users/christiaan/Desktop/Solcor/dataMergeWeek/El Arenal/El Arenal'

dataList = DL.fetchFilesforProject(newPath)
dataList2 = DL.fetchFilesforProject(newPath2)
dataList3 = DL.fetchFilesforProject(newPath3)
dataList4 = DL.fetchFilesforProject(newPath4)
#dataList5 = DL.fetchFilesforProject(newPath5)
#dataList6 = DL.fetchFilesforProject(newPath6)
#print('DL',dataList6)





d1 = "2017-05-01 00:00:00"
d2 = "2017-05-07 23:00:00"

lat = -33.447487
lng = -70.673676
magnification=50


kWhPerDay = CE.getkWhPerDay(dataList)
totalkWh = CE.getTotalkWh(dataList)
means = CE.returnAverageCloudData(d1,d2,-33.5041,-70.7109)
rain = CE.returnAverageRainData(d1,d2,-33.5041,-70.7109)


TotalData=[dataList,dataList2,dataList3,dataList4]
'''



def showProjectMenu(TotalData,means,magnification,kWhPerDay,totalkWh,rain):
    #curdoc().clear()
    list= createPlots(TotalData,means,magnification,kWhPerDay,totalkWh,rain)



    #####MAKE OVERALL LAYOUT OF ALL THE PROJECTS
    #l = layout(list, sizing_mode='fixed')
    listOfProjects=[]
    i=0
    tabu=None
    for panel in list:
        tab = Panel(child=panel,title=TotalData[i][0])
        listOfProjects.append(tab)
        i+=1
        tabu=panel

    #projects = Tabs(tabs=listOfProjects)
    #curdoc._state._reset_with_doc(projects)
    #curdoc.delete_modules()


    buttonAddNewProject = Button(label="Add new project")
    buttonAddNewProject.on_click(createNewProjectScreen())

    currentLayout.children = [list[0]]
    #curdoc().add_root(projects)




########
        #############

import urlparse, urllib

def path2url(path):
    return urlparse.urljoin(
      'file:', urllib.pathname2url(path))

def showProjectScreen(project,kWhPerDay,totalkWh,cloudData,rain):


        p = figure(width=1200, height=500,title=project.name+': global overview kW',x_axis_type='datetime',x_axis_label='Time',y_axis_label='kW')
        p.title.text_font_size='15pt'


        #p.extra_y_ranges = {"foo": Range1d(start=0, end=200)}
        #p.add_layout(LinearAxis(y_range_name="foo"), 'right')
        p.xaxis.major_label_orientation = math.pi/4

        p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
            )

####ADD kW DATA
        df = project.inverterData
        dfMax=df.max().max()
        p.y_range=Range1d(-0.5, 1.3*dfMax)



        lst = ['green', 'blue','orange','grey']
        colorPool = cycle(lst)
        for inverter in project.inverterData.columns.values:
            p.line(x=df.index.values,y=df[inverter],legend=inverter,color=next(colorPool))


        #hp = Horizon(df,plot_width=800, plot_height=500,
        #     title="horizon plot using stock inputs")


#####ADD Cloud DATA
        print('cloudData',cloudData)
        amountOfCloudDays = len([x for x in cloudData if x >= cloudyDaythresholdPercentage])

        amountOfCloudyDaysTxt = Div(text="""<p style="font-size:20px"> Cloudy days: """+str(amountOfCloudDays),
        width=300, height=30)

        cloudDataShiftIndex = cloudData.index + pd.DateOffset(hours=12)

        #l0 = p.circle(x=cloudData.index.values, y=cloudData*magnification, line_width=10,color='grey')
        meansLabel = [str(int(round(100*(x),0)))+'%' for x in cloudData.values.tolist()]

        source = ColumnDataSource(data=dict(x=cloudDataShiftIndex,
                                    y=cloudData*0,
                                    names=meansLabel))



        cloudLabels = LabelSet(x='x', y='y', text='names', level='glyph',x_offset=-5, y_offset=14*(1*dfMax),source=source, render_mode='canvas',text_font_size="10pt",text_color='grey')
        p.add_layout(cloudLabels)

#######ADD RAIN DATA

        amountOfRainDays = len([x for x in rain if x >= rainyDaythresholdPercentage])
        amountOfRainyDaysTxt = Div(text="""<p style="font-size:20px"> Rainy days: """+str(amountOfRainDays),
        width=300, height=30)
        rainDataShiftIndex = rain.index + pd.DateOffset(hours=12)
        #l0 = p.circle(x=cloudData.index.values, y=cloudData*magnification, line_width=10,color='grey')
        rainLabel = [str(int(round(100*(x),0)))+'%' for x in rain.values.tolist()]

        rainSource = ColumnDataSource(data=dict(x=rainDataShiftIndex,
                                    y=rain*0,
                                    names=rainLabel))

        rainLabels = LabelSet(x='x', y='y', text='names', level='glyph',x_offset=-5, y_offset=14*(1.05*dfMax),source=rainSource, render_mode='canvas',text_font_size="10pt",text_color='blue')
        p.add_layout(rainLabels)


####ADD kuis DATA
        NrOfDates = len(project.cleaningDates)
        shiftedCleaningDates = [x+pd.DateOffset(hours=12) for x in project.cleaningDates]
        cleaningLabels = p.circle(x=shiftedCleaningDates,y=[dfMax]*NrOfDates,line_color='orange',line_width=15,legend='cleaning')


####ADD check box
        checkbox = CheckboxGroup(labels=["meteo", "Cleaning"],
                                 active=[1,1,1], width=100)
        checkbox.callback = CustomJS(args=dict(line0=cloudLabels,line1=cleaningLabels, line2=rainLabels), code="""
            //console.log(cb_obj.active);
            line0.visible = false;
            line1.visible = false;
            line2.visible= false;
            for (i in cb_obj.active) {
                //console.log(cb_obj.active[i]);
                if (cb_obj.active[i] == 0) {
                    line0.visible = true;
                    line2.visible = true;
                } else if (cb_obj.active[i] == 1) {
                    line1.visible = true;
                }
            }
            """)

        p.legend.orientation = "horizontal"
        p.legend.location=(0,16*dfMax)
        sidePanel = column(children=[amountOfCloudyDaysTxt,amountOfRainyDaysTxt])
        divX = Div(text="""<hr noshade size=4 color=green>""",
        width=1200, height=30)

        lay2 = row([p,checkbox])
        graph1 = column([lay2,sidePanel,divX])


##################################################

        p2 = figure(width=1200, height=500,title=project.name+': global overview kWh & kWh/kWP',x_axis_type='datetime',x_axis_label='Time',y_axis_label='kW')
        p.title.text_font_size='15pt'


        #####ADD kWH DATA

        TotalkWhText = Div(text="""<p style="font-size:20px"> Total: """+str(int(round(totalkWh)))+""" kWh.""",
        width=300, height=30)

        TotalkWhText2 = Div(text="""<p style="font-size:20px"> Avg/day: """+str(int(round(totalkWh/len(kWhPerDay.index.values))))+""" kWh.""",
        width=300, height=30)

        totalKWhPerday = kWhPerDay.sum(axis=1)
        totalKWhPerday.index = totalKWhPerday.index + pd.DateOffset(hours=12)
        p2.line(x=totalKWhPerday.index.values,y=totalKWhPerday,color='red')








        globalLayout = column([graph1,p2])

        globNewLayout.children = []
        globNewLayout.children =[globalLayout]





def goToHomescreen():
    homescreen(False)

def collectData():
    generalData = [str(x.value) for x in [projectNameTxt,projectOrientation,projectInclination,projectLatitude,projectLongitude]]
    totalData = [str(x.value) for x in [total,totalkw,totAvg,totExtra]]
    inverter1Data =[str(x.value) for x in [inverter1Type,inverter1Tot,inverter1Totkw,inverter1Avg,inverter1Extra,filePick1,fileColumn1] ]
    inverter2Data = [str(x.value) for x in [inverter2Type,inverter2Tot,inverter2Totkw,inverter2Avg,inveter2Extra,filePick2,fileColumn2]]
    InverterData = [inverter1Data,inverter2Data]
    cleaningData = [pd.to_datetime(x.value) for x in [cleaningDate]]
    ExtraData = extraComments.value

    project = PE.createProject(generalData,totalData,InverterData,cleaningData,ExtraData)
    inputData=(project.name,project.inverterData)

    kWhPerDay = CE.getkWhPerDay(inputData)
    totalkWh = CE.getTotalkWh(inputData)


    projectDateBeginString=str(projectDateBegin.value)
    projectDateEndString =str(projectDateEnd.value)

    cloudData = CE.returnAverageCloudData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)
    rain = CE.returnAverageRainData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)

    showProjectScreen(project,kWhPerDay,totalkWh,cloudData,rain)





def createNewProjectScreen(quickReport=False):
    global globNewLayout
    global projectNameTxt,projectOrientation,projectInclination,projectLatitude,projectLongitude,projectDateBegin,projectDateEnd,total,totalkw,totAvg,totExtra
    global inverter1Type,inverter1Tot,inverter1Totkw,inverter1Avg,inverter1Extra,filePick1,inverter2Type,inverter2Tot,inverter2Totkw,inverter2Avg,inveter2Extra,filePick2
    global cleaningDate,extraComments
    div0 = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)
    global fileColumn1,fileColumn2


    projectNameTxt = TextInput(value="NDC", title="Project name:")
    projectOrientation =TextInput(value="0", title="Project orientation:")
    projectInclination = TextInput(value="0", title="Project inclination:")
    projectLatitude = TextInput(value="-33.447487", title="Project latitude:")
    projectLongitude = TextInput(value="-70.673676", title="Project longitude:")
    projectDateBegin = TextInput(value="2017-05-01 00:00:00", title="Begin date report:")
    projectDateEnd = TextInput(value="2017-05-07 23:45:00", title="End date report:")

    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    total = TextInput(value="46", title="Total installed cap [kWP]:")
    totalkw = TextInput(value="45", title="Total installed cap [kW]:")
    totAvg = TextInput(value="", title="Total average daily:")
    totExtra = TextInput(value="", title="Total Extra:")


    div2 = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    inverter1Type = TextInput(value="Inverter type 1", title="Inverter 1 type:")


    inverter1Tot = TextInput(value="25,5", title="Inverter 1 installed cap [kWP]:")
    inverter1Totkw = TextInput(value="25", title="Inverter 1 installed cap [kW]:")
    inverter1Avg = TextInput(value="", title="Inverter 1 average daily:")
    inverter1Extra = TextInput(value="", title="Inverter 1 EXTRA:")

    filePick1 = TextInput(value="/Users/christiaan/Desktop/Solcor/dataMergeWeek/Puratos/Inverter 1", title="Inverter 1 data:")
    fileColumn1 = TextInput(value="1", title="Inverter 1 column nr in file:")
    filePick2 = TextInput(value="/Users/christiaan/Desktop/Solcor/dataMergeWeek/Puratos/Inverter 3", title="Inverter 2 data:")
    fileColumn2 = TextInput(value="", title="Inverter 2 column nr in file:")

    div3 = Div(text="""<hr noshade size=4 color=green>""",width=1000, height=30)

    inverter2Type = TextInput(value="type 2", title="Inverter 2 type:")

    inverter2Tot = TextInput(value="20,5", title="Inverter 2 installed cap [kWP]:")
    inverter2Totkw = TextInput(value="20", title="Inverter 2 installed cap [kW]:")
    inverter2Avg = TextInput(value="", title="Inverter 2 average daily:")
    inveter2Extra = TextInput(value="", title="Inverter 2 EXTRA:")

    cleaningDate = TextInput(value="2017-05-06", title="Cleaning date:")
    extraComments = TextInput(value="Here is a comment...", title="Comments:")


    buttonBack = Button(label="Back")
    buttonBack.on_click(goToHomescreen)

    nextButton = None
    if quickReport:
        nextButton=Button(label='Next')
        nextButton.on_click(collectData)
    else:
        nextButton = Button(label='Add project')

    newLayout = [[projectNameTxt],[projectLatitude,projectLongitude],[projectOrientation,projectInclination,projectDateBegin,projectDateEnd],[],[div],[total,totalkw,totAvg,totExtra],[div2],[inverter1Type,filePick1,fileColumn1],[inverter1Tot,inverter1Totkw,inverter1Avg,inverter1Extra],[div3],[inverter2Type,filePick2,fileColumn2],[inverter2Tot,inverter2Totkw,inverter2Avg,inveter2Extra],[cleaningDate],[extraComments],[nextButton,buttonBack]]

    globNewLayout.children = []
    globNewLayout.children=[layout(newLayout)]

def function_to_call(attr, old, new):
    return None
def homescreen(firstTime):
    global globNewLayout
    welcomeTxt = Div(text="""<p style="font-size:20px;text-align: center"> Solcor operational dashboard """,
            width=1000, height=30)

    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)

    buttonOngoingProjects = Button(label="Project dashboard",)
    #buttonOngoingProjects.on_click(partial(showProjectMenu, TotalData,means,magnification,kWhPerDay,totalkWh,rain))

    buttonAddNewProject = Button(label="Add new project")
    buttonAddNewProject.on_click(partial(createNewProjectScreen,))

    menu = [("Project 1", "item_1"), ("Project 2", "item_2"), ("Project 3", "item_3")]

    manageDropDown = Dropdown(label="Manage projects", button_type="warning", menu=menu)

    inspectdropdown = Dropdown(label="Inspect Projects", button_type="warning", menu=menu)

    buttonShowDashboard = Button(label="Dashboard")

    buttonCreateQuickReport = Button(label="Create quick report")
    buttonCreateQuickReport.on_click(partial(createNewProjectScreen,quickReport=True))


    inspectdropdown.on_change('value', function_to_call)
    inspectdropdown.on_click(function_to_call)



    #url = path2url('Users/christiaan/PycharmProjects/dataMerger/static/SolcorBanner2.png')
    #print(url)

    divPicture = Div(text="<img src=https://dl.dropboxusercontent.com/s/kv1p5r6hvjpwi4z/Solcor%20logo.jpg?dl=0>")

    lay = layout([[divPicture],[welcomeTxt],[div],[buttonAddNewProject,manageDropDown],[buttonShowDashboard,inspectdropdown,buttonCreateQuickReport]])

    if firstTime:
        globNewLayout=lay
        curdoc().add_root(globNewLayout)
    else:
        globNewLayout.children = []
        globNewLayout.children =[lay]


homescreen(True)

curdoc().title = "Solcor operations"





