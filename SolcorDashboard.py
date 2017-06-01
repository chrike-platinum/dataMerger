# -*- coding: utf-8 -*-
__author__ = 'christiaan'

local_encoding = 'cp850'





from bokeh.layouts import widgetbox, row, column, layout
from bokeh.models.widgets import CheckboxGroup
from bokeh.models import Button, HoverTool
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Panel, Tabs, Paragraph, Div
import CalculationEngine as CE
from bokeh.models import CustomJS
from bokeh.models import DatetimeTickFormatter
import pandas as pd
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from itertools import cycle
from bokeh.models import LinearAxis, Range1d
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
import math
from bokeh.models import SingleIntervalTicker, LinearAxis
from bokeh.models.widgets import Select
import time
import bokeh.io as BIO
from bokeh.embed import components
from bokeh.embed import file_html
import matplotlib.pyplot as plt
import numpy as np
import re
import matplotlib.dates as mdates
from bokeh.models import Legend


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

        p = figure(width=1200, height=500,title=project[0],x_axis_type='datetime',toolbar_sticky=False)
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




#####################

import urlparse, urllib

def path2url(path):
    return urlparse.urljoin(
      'file:', urllib.pathname2url(path))


def createReadableDate(date):
    date = pd.to_datetime(date)
    date = date.date()
    date = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%d/%m/%Y')
    return date




def createInfoBanner(project,projectDateBeginString,projectDateEndString,reportNumber):
        projectDateBeginString=createReadableDate(projectDateBeginString)
        projectDateEndString=createReadableDate(projectDateEndString)
        titleTxt = Div(text="""<p style="font-size:38px ;text-align: center"> """+str(project.name),
        width=1200, height=20)
        dateTxt = Div(text="""<p style="font-size:30px ;text-align: center"> """+projectDateBeginString+" - "+projectDateEndString,
        width=1200, height=20)




        divBan = Div(text="""<hr noshade size=4 color=green>""",
        width=1200, height=10)

        titleBanner = column([titleTxt,dateTxt,divBan])

        generalTxt = Div(text="""<u><p style="font-size:20px;text-align: center""> General information:""",
        width=600, height=15)

        dateTxt = Div(text="""<p style="font-size:16px">Date: """+time.strftime("%d/%m/%Y"),
        width=600, height=15)

        reportTxt = Div(text="""<p style="font-size:16px">Report number: """+reportNumber,
        width=600, height=15)

        contactTxt = Div(text="""<p style="font-size:16px">Contact person: """+str(project.contactPerson),
        width=600, height=15)

        addressTxt = Div(text="""<p style="font-size:16px"> Address: """+str(project.street)+" "+str(project.city),
        width=600, height=15)

        telephoneTxt = Div(text="""<p style="font-size:16px"> Telephone: """+str(project.telephoneNumber),
        width=600, height=15)

        CoorTxt = Div(text="""<p style="font-size:16px"> Longitude/latitude: """+str(project.projectLongitudeString)+" / "+str(project.projectLatitudeString),
        width=600, height=15)

        generalInfo = column([generalTxt,reportTxt,dateTxt,contactTxt,addressTxt,telephoneTxt,CoorTxt])

        siteTxt = Div(text="""<u><p style="font-size:20px;text-align: center""> Site information:""",
        width=600, height=20)

        installedCapTxt = Div(text="""<p style="font-size:16px"> Installed capacity: """+str(project.totalkWP)+" kWP",
        width=600, height=15)

        installedCapkWTxt = Div(text="""<p style="font-size:16px"> Nominal Installed capacity: """+str(project.totalkw)+" kW",
        width=600, height=15)

        installationOrienTxt = Div(text="""<p style="font-size:16px"> Orientation/Inclination: """+str(project.projectOrientation)+"° / "+str(project.projectInclination)+'°',
        width=600, height=15)

        structureTxt = Div(text="""<p style="font-size:16px"> Structure: """+str(project.structureType),
        width=600, height=15)


        siteInfo = column([siteTxt,installedCapTxt,installedCapkWTxt,installationOrienTxt,structureTxt])


        allInfo = row([generalInfo,siteInfo])

        banner = column([titleBanner,allInfo])

        return banner

def createInfoPart(project,listTitleLeft,listLeft,listTitleRight,listRight):

    divTitleLeft = Div(text="""<u><p style="font-size:20px;text-align: center""> """+listTitleLeft,
        width=600, height=20)

    divListLeft = [divTitleLeft]
    for info in listLeft:
        divListLeft.append(Div(text="""<p style="font-size:16px"> """+str(info[0])+": "+str(info[1]),
        width=600, height=15))

    leftInfoList = column(divListLeft)

    divTitleRight = Div(text="""<u><p style="font-size:20px;text-align: center""> """+listTitleRight,
        width=600, height=20)


    divListRight = [divTitleRight]
    for info in listRight:
        divListRight.append(Div(text="""<p style="font-size:16px"> """+str(info[0])+": "+str(info[1]),
        width=600, height=15))


    rightInfoList = column(divListRight)


    allInfo = row([leftInfoList,rightInfoList])
    return column([allInfo])


def createInfoTitle(title):
    divTitle = Div(text="""<p style="font-size:28px ;text-align: center"> """+title,
        width=1200, height=16)
    divLine = Div(text="""<hr noshade size=4 color=green>""",
        width=1200, height=10)

    return column([divTitle,divLine])


def createInfoInverterPart(project,title,listTitleLeft,listLeft,listTitleRight,listRight):
    divTitle = Div(text="""<p style="font-size:28px ;text-align: center; color:green"><u> """+title,
        width=1200, height=16)


    divTitleLeft = Div(text="""<u><p style="font-size:20px;text-align: center""> """+listTitleLeft,
        width=600, height=20)

    divListLeft = [divTitleLeft]
    for info in listLeft:
        divListLeft.append(Div(text="""<p style="font-size:16px"> """+str(info[0])+": "+str(info[1]),
        width=600, height=15))

    leftInfoList = column(divListLeft)

    divTitleRight = Div(text="""<u><p style="font-size:20px;text-align: center""> """+listTitleRight,
        width=600, height=20)


    divListRight = [divTitleRight]
    for info in listRight:
        divListRight.append(Div(text="""<p style="font-size:16px"> """+str(info[0])+": "+str(info[1]),
        width=600, height=15))



    rightInfoList = column(divListRight)

    #divLine = Div(text="""<hr noshade size=2 align="center">""",
    #    width=800, height=10)


    allInfo = row([leftInfoList,rightInfoList])
    return column([divTitle,allInfo])


def createInverterPlots(kWhPerDay,project,projectDateBeginString,projectDateEndString):
    fig = plt.figure(figsize=(12,5))
    ax = fig.add_subplot(111)
    TOOLS = 'pan,box_zoom,wheel_zoom,save,box_select,crosshair,resize,undo,redo,reset'
    p3 = figure(width=1200, height=500,x_axis_type='datetime',x_axis_label='Time',y_axis_label='kWh/kWP',tools=TOOLS,toolbar_sticky=False)
    p3.toolbar.active_drag = "auto"
    p3.toolbar.active_scroll = "auto"
    ax.set_ylabel('kWh/kWP')
    ax.set_xlabel('Time')
    p3.title.text_font_size='15pt'
    p3.xaxis.major_label_orientation = math.pi/4

    p3.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
            )
    lst = ['green', 'blue','orange','red','yellow','purple','grey','black']
    colorPool = cycle(lst)
    inverterID=0
    month = datetime.datetime.strptime(projectDateBeginString,'%Y-%m-%d %H:%M:%S').month
    avgkwhKWP = project.getDailyAverageKWhKWp(projectDateBeginString,projectDateEndString)
    plotDates=[]
    plotlines = []
    for inverterName in kWhPerDay.columns.values:
        kWhPerDay2=kWhPerDay[kWhPerDay.columns[inverterID]]/project.invertersTotKWP[inverterID]
        color = next(colorPool)
        line = p3.line(x=kWhPerDay2.index.values,y=kWhPerDay2,color=color)
        plotlines.append(('Inv '+str(inverterID+1),[line]))
        plotDates = [createReadableDate(date) for date in kWhPerDay2.index.values]
        plotDates = [datetime.datetime.strptime(d,'%d/%m/%Y').date() for d in plotDates]
        ax.plot(plotDates,kWhPerDay2,label='Inv '+str(inverterID),color=color,linewidth='1')
        #avg = [avgkwhKWP]*len(kWhPerDay.index.values)#/project.invertersTotKWP[inverterID]]*len(kWhPerDay.index.values)
        #p3.line(x=kWhPerDay2.index.values,y=avg,legend='Inv '+str(inverterID+1)+' (avg)',color='light'+color)
        #plt.plot(kWhPerDay2.index.values,avg,label='Inv '+str(inverterID)+' (avg)',color='light'+color)
        inverterID +=1
    avg = [avgkwhKWP]*len(kWhPerDay.index.values)
    avgLine = p3.line(x=kWhPerDay2.index.values,y=avg,color='black')
    plotlines.append(('Exp. avg.',[avgLine]))

    ax.plot(plotDates,avg,label='Exp. avg.',color='black',linewidth='1')
    #ax = plt.subplot(111)
    #ax.grid()


    #p3.line(x=kWhPerDay.index.values,y=kWhPerDay,legend='I '+str(inverterID)+': inverterName')

    minkWP=min(project.invertersTotKWP)
    dfMaxkWh=(kWhPerDay/minkWP).max().max()
    p3.y_range=Range1d(-0.5, 1.2*dfMaxkWh)


    legend2 = Legend(items=plotlines,location=(55, 0)) #-30
    p3.add_layout(legend2, 'above')
    p3.legend.click_policy="hide"
    p3.legend.orientation = "horizontal"





    ax.set_xticks(plotDates)
    ax.set_xticklabels(plotDates,rotation=45,ha='right',fontsize=8)
    ax.grid(linewidth=0.5,which='major')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=4, fancybox=True)
    myFmt = mdates.DateFormatter('%d %B %Y')
    ax.xaxis.set_major_formatter(myFmt)

    fig.savefig('plot.png', bbox_inches='tight')


    p3.xaxis[0].ticker=DatetimeTicker(desired_num_ticks=len(kWhPerDay))

    leftlist = []
    rightlist = []
    info2div = createInfoTitle('Inverter: overview kWh/kWP')
    inverterID2=0
    inverterLayout = []
    for inverterName in kWhPerDay.columns.values:
        totalGenerated = kWhPerDay[kWhPerDay.columns[inverterID2]].sum()
        avgkwhKWP = avgkwhKWP




        percentage = round(project.getPercentageChange(projectDateBeginString,projectDateEndString),2)
        ExpectedProductionHorizontal = round(project.getDailyAverageKWhKWp(projectDateBeginString,projectDateEndString),2)*len(kWhPerDay.index.values)
        InplaneProduction=percentage*ExpectedProductionHorizontal
        InplaneProductionkWh = InplaneProduction*project.invertersTotKWP[inverterID2]

        PR = round((totalGenerated/project.invertersTotKWP[inverterID2])/InplaneProduction,3)*100

        leftlist = [('Performance ratio',str(PR)+'%'),('Total production',str(int(round(totalGenerated)))+' kWh'),
                     ('Expected production',str(int(round(InplaneProductionkWh)))+ ' kWh'),('Real daily average',str((round(totalGenerated/project.invertersTotKWP[inverterID2]/len(kWhPerDay.index.values),2)))+' kWh/kWP')]

        rightlist=[('Inverter type',str(project.inverterTypes[inverterID2])),('Installed capacity',str(project.invertersTotKWP[inverterID2])+' kWP'),('Nominal installed capacity',str(project.invertersTotkw[inverterID2])+' kW'),
                   ('Expected daily average',str(round((avgkwhKWP*percentage),2))+' kWh/kWP'),('Expected daily average',str(round((avgkwhKWP*percentage*project.invertersTotKWP[inverterID2]),2))+' kWh')]

        inverterLayout.append(createInfoInverterPart(project,'inverter '+str(inverterID2+1),'Performance indicators:',leftlist,'Inverter information:',rightlist))
        inverterID2+=1

    inverterLayout=column(inverterLayout)
    print(inverterLayout)
    inverterGraph=[info2div,p3,inverterLayout]

    return inverterGraph





def showProjectScreen(reportNumber,project,kWhPerDay,totalkWh,cloudData,rain,projectDateBeginString,projectDateEndString):

        banner = createInfoBanner(project,projectDateBeginString,projectDateEndString,reportNumber)

        p = figure(width=1200, height=500,x_axis_type='datetime',x_axis_label='Time',y_axis_label='kW',toolbar_sticky=False)
        p.title.text_font_size='15pt'

        fig3 = plt.figure(figsize=(12,5))
        ax1 = fig3.add_subplot(111)
        ax1.set_ylabel('kW')
        ax1.set_xlabel('Time')



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
        df = project.getInverterDatafromTo(projectDateBeginString,projectDateEndString)
        dfMax=df.max().max()
        p.y_range=Range1d(-0.5, 1.3*dfMax)



        lst = ['green', 'blue','orange','grey','red','purple']
        colorPool = cycle(lst)

        lineLegends=[]
        inverterID3=1
        plotDates = [date for date in df.index.values]
        plotDates = [date for date in plotDates]# if (pd.Timestamp(date).time().strftime('%H:%M:%S')=='00:00:00')]
        plotDates2 = [date for date in plotDates if (pd.Timestamp(date).time().strftime('%H:%M:%S')=='00:00:00')]
        #plotDates = [datetime.datetime.strptime(d,'%d/%m/%Y %H:%m:%S').date() for d in plotDates]
        #plotDates = [createReadableDate(date) for date in plotDates]


        for inverter in project.inverterData.columns:
            color = next(colorPool)
            line = p.line(x=df.index.values,y=df[inverter],color=color)
            ax1.plot(plotDates,df[inverter],label='Inv '+str(inverterID3),color=color,linewidth='1')
            inverterID3+=1
            lineLegends.append(('Inv '+str(inverterID3),[line]))


        #hp = Horizon(df,plot_width=800, plot_height=500,
        #     title="horizon plot using stock inputs")


#####ADD Cloud DATA
        amountOfCloudDays = len([x for x in cloudData if x >= cloudyDaythresholdPercentage])
        cloudDataShiftIndex = cloudData.index + pd.DateOffset(hours=12)

        #l0 = p.circle(x=cloudData.index.values, y=cloudData*magnification, line_width=10,color='grey')
        meansLabel = [str(int(round(100*(x),0)))+'%' for x in cloudData.values.tolist()]


        beginLabelCloud = cloudDataShiftIndex.values[0] - np.timedelta64(1, 'D')

        cloudDataShiftIndex = np.insert(cloudDataShiftIndex,0,beginLabelCloud)
        source = ColumnDataSource(data=dict(x=cloudDataShiftIndex,
                                    y=np.append(cloudData*0+dfMax,[cloudData[0]*0+dfMax]),
                                    names=['cloud']+meansLabel))



        cloudLabels = LabelSet(x='x', y='y', text='names', level='glyph',x_offset=-5, y_offset=17,source=source, render_mode='canvas',text_font_size="10pt",text_color='grey')
        p.add_layout(cloudLabels)

#######ADD RAIN DATA

        amountOfRainDays = len([x for x in rain if x >= rainyDaythresholdPercentage])
        rainDataShiftIndex = rain.index + pd.DateOffset(hours=12)
        #l0 = p.circle(x=cloudData.index.values, y=cloudData*magnification, line_width=10,color='grey')
        rainLabel = [str(int(round(100*(x),0)))+'%' for x in rain.values.tolist()]


        beginLabelRain = rainDataShiftIndex.values[0] - np.timedelta64(1, 'D')
        #rainDataShiftIndex = np.insert(rainDataShiftIndex,0,beginLabelRain)
        rainDataShiftIndex = np.r_[beginLabelRain, rainDataShiftIndex]
        rainSource = ColumnDataSource(data=dict(x=rainDataShiftIndex,
                                    y=np.append(rain*0+dfMax,[rain[0]*0+dfMax]),
                                    names=['Rain']+rainLabel))

        rainLabels = LabelSet(x='x', y='y', text='names', level='glyph',x_offset=-5, y_offset=30,source=rainSource, render_mode='canvas',text_font_size="10pt",text_color='blue')
        p.add_layout(rainLabels)
######fill info banner
        leftlist = [('Number of cloudy days',amountOfCloudDays),('Number of rainy days',amountOfRainDays)]

        cleaningDatesString=[createReadableDate(str(cleaning.date())) for cleaning in project.cleaningDates]
        internetProbString = [createReadableDate(str(internetProb.date())) for internetProb in project.internetProblems]
        gridProbString = [createReadableDate(str(gridProb.date())) for gridProb in project.gridProblemData]
        maintenaceString = [createReadableDate(str(maintenace.date())) for maintenace in project.maintenanceData]
        extraCommentString = [str(comment) for comment in project.commentList]


        rightlist = [('Cleaning dates',str(cleaningDatesString)),('Internet Problems dates',str(internetProbString)),
                     ('Grid Problems dates',str(gridProbString)),('Maintenance dates',str(maintenaceString)),('Comment',str(extraCommentString))]
        titleDiv = createInfoTitle('Global overview kW')
        inf = createInfoPart(project,'Weather information:',leftlist,'Maintenance information:',rightlist)


####ADD clean DATA
        NrOfDates = len(project.cleaningDates)
        shiftedCleaningDates = [x+pd.DateOffset(hours=12) for x in project.cleaningDates]
        cleaningLabels = p.circle(x=shiftedCleaningDates,y=[1.03*dfMax]*NrOfDates,line_color='orange',line_width=10)
        lineLegends.append(('cleaning',[cleaningLabels]))


        NrOfDatesG = len(project.gridProblemData)
        shiftedGridProbDates = [x+pd.DateOffset(hours=12) for x in project.gridProblemData]
        gribProdLabels = p.circle(x=shiftedGridProbDates,y=[1.03*dfMax]*NrOfDatesG,line_color='red',line_width=10)


        NrOfDatesM = len(project.maintenanceData)
        shiftedmaintanenanceDates = [x+pd.DateOffset(hours=12) for x in project.maintenanceData]
        maintenanceLabels = p.circle(x=shiftedmaintanenanceDates,y=[1.03*dfMax]*NrOfDatesM,line_color='red',line_width=10)

        NrOfDatesI = len(project.internetProblems)
        shiftedinternetProbDates = [x+pd.DateOffset(hours=12) for x in project.internetProblems]
        internetProbLabels = p.circle(x=shiftedinternetProbDates,y=[1.03*dfMax]*NrOfDatesI,line_color='red',line_width=10)
        lineLegends.append(('Problem',[gribProdLabels,maintenanceLabels,internetProbLabels]))


####ADD check box
        checkbox = CheckboxGroup(labels=["Meteo", "Info"],
                                 active=[0,1], width=100)
        checkbox.callback = CustomJS(args=dict(line0=cloudLabels,line1=cleaningLabels,line3=gribProdLabels,line4=maintenanceLabels,line5=internetProbLabels, line2=rainLabels), code="""
            //console.log(cb_obj.active);
            line0.visible = false;
            line1.visible = false;
            line3.visible = false;
            line4.visible = false;
            line5.visible = false;
            line2.visible= false;
            for (i in cb_obj.active) {
                //console.log(cb_obj.active[i]);
                if (cb_obj.active[i] == 0) {
                    line0.visible = true;
                    line2.visible = true;
                } else if (cb_obj.active[i] == 1) {
                    line1.visible = true;
                    line3.visible = true;
                    line4.visible = true;
                    line5.visible = true;
                }
            }
            """)

        legend2 = Legend(items=lineLegends,location=(55, 0)) #-30
        p.add_layout(legend2, 'above')
        p.legend.click_policy="hide"
        p.legend.orientation = "horizontal"

        ax1.set_xticks(plotDates2[0::1],minor=False)
        ax1.set_xticks(plotDates2[1::2],minor=True)
        ax1.set_xticklabels(plotDates2,rotation=45,ha='right',fontsize=8)
        ax1.xaxis.grid(linewidth=0.5,which='minor')
        ax1.yaxis.grid(linewidth=0.5,which='major')
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
              ncol=4, fancybox=True)
        myFmt = mdates.DateFormatter('%d %B %Y')
        ax1.xaxis.set_major_formatter(myFmt)

        fig3.savefig('plot3.png', bbox_inches='tight')



        p.xaxis[0].ticker=DatetimeTicker(desired_num_ticks=len(cloudData))


        lay2 = row([p,checkbox])
        globalkWGraph = column([banner,titleDiv,lay2,inf])


##################################################
        fig2 = plt.figure(figsize=(12,5))
        ax1 = fig2.add_subplot(111)
        ax1.set_ylabel('kWh',color='blue')
        ax1.set_xlabel('Time')
        ax2 = ax1.twinx()
        ax2.set_ylabel('kWh/kWP', color='green')



        p2 = figure(width=1200, height=500,x_axis_type='datetime',x_axis_label='Time',y_axis_label='kWh',toolbar_sticky=False)
        p2.title.text_font_size='15pt'
        p2.xaxis.major_label_orientation = math.pi/4

        p2.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
            )



        #####ADD kWh DATA


        totalKWhPerday = kWhPerDay.sum(axis=1)

        totalKWhPerday = totalKWhPerday.to_frame()
        totalKWhPerday.columns = ['kWh']
        totalKWhPerday.index = pd.to_datetime(totalKWhPerday.index) #+ pd.DateOffset(hours=12)
        df = totalKWhPerday
        dfMaxkWh=df.max().max()
        dfMaxkWhkWP=(df/project.totalkWP).max().max()
        yValues=df[df.columns[0]]

        p2.y_range=Range1d(-0.5, 1.2*dfMaxkWh)
        p2.extra_y_ranges = {"etxraAxis": Range1d(start=0, end=2*dfMaxkWhkWP)}
        lineLegends2=[]

        plotDates = [createReadableDate(date) for date in df.index.values]
        plotDates = [datetime.datetime.strptime(d,'%d/%m/%Y').date() for d in plotDates]

        kwhLine = p2.line(x=df.index.values,y=yValues,color='blue')
        ax1.plot(plotDates,yValues,label='kWh',color='blue',linewidth='1')

        lineLegends2.append(('kWh',[kwhLine]))
        p2.yaxis.axis_label_text_color = "blue"
        p2.add_layout(LinearAxis(y_range_name="etxraAxis",axis_label='kWh/kWP',axis_label_text_color='green'), 'right')

        p2.xaxis[0].ticker=DatetimeTicker(desired_num_ticks=len(cloudData))




        percentage = round(project.getPercentageChange(projectDateBeginString,projectDateEndString),2)
        projectAVG=project.getDailyAverageKWhKWp(projectDateBeginString,projectDateEndString)*percentage


        ###ADD Averages


        yvaluesAVG = [projectAVG*project.totalkWP]*len(yValues)
        ExpAvhKwhLine = p2.line(x=df.index.values,y=yvaluesAVG,color='lightblue',line_width=2)
        kwhKWPLIne = p2.line(x=df.index.values,y=yValues/project.totalkWP,color='green',y_range_name="etxraAxis")



        ax2.plot(plotDates,yValues/project.totalkWP,label='kWh/kWP',color='green',linewidth='1')
        ax1.plot(plotDates,yvaluesAVG,label='Exp. Avg. kWh',color='lightblue',linewidth='1')


        lineLegends2.append(('Exp. Avg. kWh',[ExpAvhKwhLine]))
        lineLegends2.append(('kWh/kWP',[kwhKWPLIne]))




        yValueskWP=[projectAVG]*len(yValues)#[x/project.totalkWP for x in yvaluesAVG]
        ExpKWhKWP= p2.line(x=df.index.values,y=yValueskWP,y_range_name="etxraAxis",color='lightgreen',line_width=2)
        ax2.plot(plotDates,yValueskWP,label='Exp. Avg. kWh/kWP',color='lightgreen',linewidth='1')

        lineLegends2.append(('Exp. Avg. kWh/kWP',[ExpKWhKWP]))



        legend3 = Legend(items=lineLegends2,location=(55, 0)) #-30
        p2.add_layout(legend3, 'above')
        p2.legend.click_policy="hide"
        p2.legend.orientation = "horizontal"


        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()




        ax1.set_ylim([-0.5, 1.2*dfMaxkWh])
        ax2.set_ylim(0,2*dfMaxkWhkWP)
        ax1.set_xticks(plotDates2[1::2],minor=True)
        ax1.set_xticklabels(plotDates,rotation=45,ha='right',fontsize=8)
        ax1.xaxis.grid(linewidth=0.5,which='minor')
        ax1.yaxis.grid(linewidth=0.5,which='major')
        ax1.legend(h1+h2, l1+l2,loc='upper center', bbox_to_anchor=(0.5, 1.1),
              ncol=4, fancybox=True)
        myFmt = mdates.DateFormatter('%d %B %Y')
        ax1.xaxis.set_major_formatter(myFmt)

        fig2.savefig('plot2.png', bbox_inches='tight')

        #BIO.output_file(filename='p2.html',mode='inline')

        #BIO.show(curdoc(), new='tab', notebook_handle=False, notebook_url='localhost:8888')

        #file = BIO.save(p2)
        #print(file)

        ###Performance indicators

        totalGenerated = totalkWh


        underperfDays = sum([1 if x<projectAVG*project.totalkWP else 0 for x in totalKWhPerday[totalKWhPerday.columns[0]]])
        overperfDays = sum([1 if x>=projectAVG*project.totalkWP else 0 for x in totalKWhPerday[totalKWhPerday.columns[0]]])



        GHIdaily= round(project.getGHI(projectDateBeginString,projectDateEndString),2)
        GIIdaily= round(project.getGII(projectDateBeginString,projectDateEndString),2)
        percentage = round(project.getPercentageChange(projectDateBeginString,projectDateEndString),2)
        dailyAvgKWhKWP= round(project.getDailyAverageKWhKWp(projectDateBeginString,projectDateEndString),2)
        monthlyExpectedProductionHorizontal = dailyAvgKWhKWP*len(df.index.values)
        InplaneProduction=percentage*monthlyExpectedProductionHorizontal



        PR = round((totalGenerated/project.totalkWP)/InplaneProduction,3)*100
        print('PR:'+str(PR))




        leftlist = [('Performance ratio',str(PR)+'%'),('GHI daily',str(GHIdaily)+' kWh/m^2'),('GII daily',str(GIIdaily)+' kWh/m^2'),('Total production',str(int(round(totalGenerated)))+' kWh'),
                     ('Real daily average',str((round(totalGenerated/project.totalkWP/len(df.index.values),2)))+' kWh/kWP')]
        rightlist = [('Expected production',str(int(round(InplaneProduction*project.totalkWP)))+ ' kWh'),('Expected daily average',str(round((dailyAvgKWhKWP*percentage),2))+' kWh/kWP'),
                     ('Expected daily average',str(round((dailyAvgKWhKWP*percentage*project.totalkWP),2))+' kWh'),('Number of underperforming days',underperfDays),('Number of overperforming days',overperfDays)]
        titDiv = createInfoTitle('Global overview kWh & kWh/kWP')
        info2div = createInfoPart(project,'Real performance indicators:',leftlist,'Estimated performance indicators:',rightlist)

        GlobalKwhGraph=column([titDiv,p2,info2div])

#########INVERTERGRAPH



        inverterGraphs =[]
        inverterGraphs.append(createInverterPlots(kWhPerDay,project,projectDateBeginString,projectDateEndString))

        inverterGraphs= [item for sublist in inverterGraphs for item in sublist]
        inverterGraphs = column(inverterGraphs)

        globalLayout = column([globalkWGraph,GlobalKwhGraph,inverterGraphs])

        globNewLayout.children = []
        globNewLayout.children =[globalLayout]


        script, div = components(curdoc())

        BIO.output_file(filename=project.name+' '+projectDateBeginString+' '+projectDateEndString+'.html',mode='inline')

        #BIO.show(curdoc(), new='tab', notebook_handle=False, notebook_url='localhost:8888')
        file = BIO.save(curdoc())
        print('File saved at:',file)


def goToHomescreen():
    homescreen(False)

def convert(tude): #DEPRECATED
    multiplier = 1 if tude[-1] in ['N', 'E'] else -1
    return multiplier * sum(float(x) / 60 ** n for n, x in enumerate(tude[:-1].split('-')))

def conversion(old):
    old.replace(' ','')
    old = old.replace(',','.')
    direction = {'N':1, 'S':-1, 'E': 1, 'W':-1}
    new = old.replace(u'°',' ').replace('\'',' ').replace('"',' ')
    new = new.split()
    new_dir = new.pop()
    new.extend([0,0,0])
    print(new)
    return (float(new[0])+float(new[1])/60.0+float(new[2])/3600.0) * direction[new_dir]




def collectData():
    checklist = ["N", "n", "W","w","E","e","S","s","O",'o','Z','z']
    if (len([e for e in checklist if e in projectLatitude.value]) >=1):
        projectLatitudeCon = conversion(projectLatitude.value.decode('utf-8'))
    else:
        projectLatitudeCon = projectLatitude.value
    if (len([a for a in checklist if a in projectLongitude.value]) >=1):
        projectLongitudeCon = conversion(projectLongitude.value.decode('utf-8'))
    else:
        projectLongitudeCon = projectLongitude.value

    generalData = [str(x.value) for x in [projectNameTxt,projectOrientation,projectInclination,structureDD]]
    geoData = [projectLatitudeCon,projectLongitudeCon,str(projectLatitude.value),str(projectLongitude.value)]
    adresData = [str(x.value) for x in [projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt]]
    totalData = [str(x.value) for x in [total,totalkw,totAvg,totExtra]]
    inverter1Data =[str(x.value) for x in [inverter1Type,inverter1Tot,inverter1Totkw,inverter1Avg,inverter1Extra,filePick1,fileColumn1] ]
    inverter2Data = [str(x.value) for x in [inverter2Type,inverter2Tot,inverter2Totkw,inverter2Avg,inveter2Extra,filePick2,fileColumn2]]
    InverterData = [inverter1Data,inverter2Data]
    cleaningData = cleaningDate.value.split(',')
    cleaningData = [datetime.datetime.strptime(x, '%d-%m-%Y') for x in cleaningData if str(pd.to_datetime(x)) != 'NaT']

    gridProbData = gridProbDate.value.split(',')
    gridProbData = [datetime.datetime.strptime(x, '%d-%m-%Y') for x in gridProbData if str(pd.to_datetime(x)) != 'NaT']

    maintanceData = maintenanceDate.value.split(',')
    maintanceData = [datetime.datetime.strptime(x, '%d-%m-%Y') for x in maintanceData if str(pd.to_datetime(x)) != 'NaT']

    internetProbData = internetProblemDate.value.split(',')
    internetProbData = [datetime.datetime.strptime(x, '%d-%m-%Y') for x in internetProbData if str(pd.to_datetime(x)) != 'NaT']


    maintancelist=[cleaningData,gridProbData,maintanceData,internetProbData]

    projectDateBeginString=str(projectDateBegin.value)
    projectDateEndString =str(projectDateEnd.value)


    ExtraData = extraComments.value
    reportNumber = str(reportNumberTxt.value)
    GHIdf = CE.collectSolarisData(solargisLocation.value,solargisYear.value)


    project = PE.createProject(generalData,geoData,totalData,InverterData,maintancelist ,ExtraData,adresData,GHIdf)
    inputData=(project.name,project.getInverterDatafromTo(projectDateBeginString,projectDateEndString))


    kWhPerDay = CE.getkWhPerDay(inputData)
    totalkWh = CE.getTotalkWh(inputData)






    cloudData = CE.returnAverageCloudData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)
    rain = CE.returnAverageRainData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)



    showProjectScreen(reportNumber,project,kWhPerDay,totalkWh,cloudData,rain,projectDateBeginString,projectDateEndString)






def createNewProjectScreen(quickReport=False):
    global globNewLayout
    global projectNameTxt,reportNumberTxt,projectOrientation,projectInclination,projectLatitude,projectLongitude,projectDateBegin,projectDateEnd,total,totalkw,totAvg,totExtra
    global projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt
    global inverter1Type,inverter1Tot,inverter1Totkw,inverter1Avg,inverter1Extra,filePick1,inverter2Type,inverter2Tot,inverter2Totkw,inverter2Avg,inveter2Extra,filePick2
    global cleaningDate,extraComments,structureDD,gridProbDate,maintenanceDate,internetProblemDate,solargisLocation,solargisYear
    div0 = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)
    global fileColumn1,fileColumn2


    projectNameTxt = TextInput(value="Nueces Del Choapa", title="Project name:")
    reportNumberTxt= TextInput(value="1", title="Report number:")

    projectContactTxt = TextInput(value="Leonardo Pasten", title="Contact person:")
    projectStreetTxt = TextInput(value="Principal el Tambo", title="Street + nr:")
    projectCityTxt = TextInput(value="Salamanca Chile", title="City (+ Country):")
    projectTelephoneTxt = TextInput(value="", title="Telephone:")

    div0 = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)

    projectOrientation =TextInput(value="-10", title="Project orientation:")
    projectInclination = TextInput(value="15", title="Project inclination:")
    projectLatitude = TextInput(value="""31° 46' 59.27" S""", title="Project latitude:")
    projectLongitude = TextInput(value="""70° 59' 3.36" W""", title="Project longitude:")




    structureDD = Select(title='Structure', value='Parallel to roof', options=["Parallel to roof","Structure with inclination"])



    projectDateBegin = TextInput(value="2017-04-01 00:00:00", title="Begin date report:")
    projectDateEnd = TextInput(value="2017-04-30 23:45:00", title="End date report:")

    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    total = TextInput(value="46", title="Total installed cap [kWP]:")
    totalkw = TextInput(value="45", title="Total installed cap [kW]:")
    totAvg = TextInput(value="4.87", title="Total exp. daily avg. [kWh/kWP]:")
    totExtra = TextInput(value="", title="Total Extra:")


    div2 = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    inverter1Type = TextInput(value="25000TL-30", title="Inverter 1 type:")


    inverter1Tot = TextInput(value="25,5", title="Inverter 1 installed cap [kWP]:")
    inverter1Totkw = TextInput(value="25", title="Inverter 1 installed cap [kW]:")
    inverter1Avg = TextInput(value="4.87", title="Inverter 1 exp. daily avg. [kWh/KWP]:")
    inverter1Extra = TextInput(value="", title="Inverter 1 EXTRA:")

    filePick1 = TextInput(value="/Users/christiaan/Desktop/Solcor/dataMergeWeek/Neuces2/Nueces/Nueces", title="Inverter 1 data:")
    fileColumn1 = TextInput(value="2", title="Inverter 1 column nr in file:")
    filePick2 = TextInput(value="/Users/christiaan/Desktop/Solcor/dataMergeWeek/Neuces2/Nueces/Nueces", title="Inverter 2 data:")
    fileColumn2 = TextInput(value="1", title="Inverter 2 column nr in file:")

    div3 = Div(text="""<hr noshade size=4 color=green>""",width=1000, height=30)

    inverter2Type = TextInput(value="20000TL-30", title="Inverter 2 type:")

    inverter2Tot = TextInput(value="20,5", title="Inverter 2 installed cap [kWP]:")
    inverter2Totkw = TextInput(value="20", title="Inverter 2 installed cap [kW]:")
    inverter2Avg = TextInput(value="4.87", title="Inverter 2 exp. daily avg. [kWh/kWP]:")
    inveter2Extra = TextInput(value="", title="Inverter 2 EXTRA:")

    div4 = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)

    cleaningDate = TextInput(value="", title="Cleaning date(s):")
    gridProbDate = TextInput(value="", title="Grid problem date(s):")
    maintenanceDate = TextInput(value="", title="Maintenance date(s):")
    internetProblemDate = TextInput(value="", title="Internet problem date(s):")





    extraComments = TextInput(value="Here is a comment...", title="Comments:")
    solargisLocation = TextInput(value='/Users/christiaan/Desktop/Solcor/dataMergeWeek/NDC_PV-8627-1705-1780_-31.783--70.984.xls', title="Solargis file location:")
    solargisYear = TextInput(value='2017', title="Solargis file year:")



    buttonBack = Button(label="Back")
    buttonBack.on_click(goToHomescreen)

    nextButton = None
    if quickReport:
        nextButton=Button(label='Next')
        nextButton.on_click(collectData)
    else:
        nextButton = Button(label='Add project')

    newLayout = [[projectNameTxt,reportNumberTxt],[projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt],[div0],[projectLatitude,projectLongitude,structureDD],[projectOrientation,projectInclination,projectDateBegin,projectDateEnd],[],
                 [div],[total,totalkw,totAvg,totExtra],[div2],[inverter1Type,filePick1,fileColumn1],[inverter1Tot,inverter1Totkw,inverter1Avg,inverter1Extra],
                 [div3],[inverter2Type,filePick2,fileColumn2],[inverter2Tot,inverter2Totkw,inverter2Avg,inveter2Extra],
                 [div4],[cleaningDate,gridProbDate,maintenanceDate,internetProblemDate],[extraComments,solargisLocation,solargisYear],[nextButton,buttonBack]]

    globNewLayout.children = []
    globNewLayout.children=[layout(newLayout)]


    #BIO.reset_output()
    #BIO.show(globNewLayout)

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

    buttonSettings = Button(label="Settings")


    inspectdropdown.on_change('value', function_to_call)
    inspectdropdown.on_click(function_to_call)



    #url = path2url('Users/christiaan/PycharmProjects/dataMerger/static/SolcorBanner2.png')
    #print(url)

    divPicture = Div(text="<img src=https://dl.dropboxusercontent.com/s/kv1p5r6hvjpwi4z/Solcor%20logo.jpg?dl=0>")

    lay = layout([[divPicture],[welcomeTxt],[div],[buttonAddNewProject,manageDropDown,buttonSettings],[buttonShowDashboard,inspectdropdown,buttonCreateQuickReport]])

    if firstTime:
        globNewLayout=lay
        curdoc().add_root(globNewLayout)
    else:
        globNewLayout.children = []
        globNewLayout.children =[lay]


homescreen(True)

curdoc().title = "Solcor operations"






