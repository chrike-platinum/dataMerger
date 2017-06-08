# -*- coding: utf-8 -*-
__author__ = 'christiaan'

local_encoding = 'cp850'
tempPlotDir = 'tempPlots/'
plotFileName = 'plot'






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
import matplotlib.pyplot as plt
import numpy as np
import re
import matplotlib.dates as mdates
from bokeh.models import Legend
import pdfMaker as PM
import urlparse, urllib
from printObject import PrintObject

printObject = PrintObject()

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

    allInfo = row([leftInfoList,rightInfoList])
    return column([divTitle,allInfo])


def createInverterPlots(kWhPerDay,project,projectDateBeginString,projectDateEndString):


    fig = plt.figure(figsize=(12,5))
    ax = fig.add_subplot(111)
    #TOOLS = 'pan,box_zoom,wheel_zoom,save,box_select,crosshair,resize,undo,redo,reset'
    p3 = figure(width=1200, height=500,x_axis_type='datetime',x_axis_label='Time',y_axis_label='kWh/kWP',toolbar_sticky=False)
    #p3.toolbar.active_drag = "auto"
    #p3.toolbar.active_scroll = "auto"
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
    plotDates=[]
    plotlines = []
    for inverterName in kWhPerDay.columns.values:
        inverter = project.getInverter(inverterID)
        kWhPerDay2=kWhPerDay[kWhPerDay.columns[inverterID]]/inverter.kWP
        color = next(colorPool)
        line = p3.line(x=kWhPerDay2.index.values,y=kWhPerDay2,color=color)
        plotlines.append(('Inv '+str(inverterID+1),[line]))
        plotDates = [createReadableDate(date) for date in kWhPerDay2.index.values]
        plotDates = [datetime.datetime.strptime(d,'%d/%m/%Y').date() for d in plotDates]
        ax.plot(plotDates,kWhPerDay2,label='Inv '+str(inverterID),color=color,linewidth='1')
        inverterID +=1

    GIIdaily= project.getGII(projectDateBeginString,projectDateEndString)

    expPR=round(project.getExpectedPR(projectDateBeginString,projectDateEndString),1)
    expDailyAvg=round(expPR*GIIdaily/100,2)

    avg = [expDailyAvg]*len(kWhPerDay.index.values)
    avgLine = p3.line(x=kWhPerDay2.index.values,y=avg,color='black')
    plotlines.append(('Exp. avg.',[avgLine]))

    ax.plot(plotDates,avg,label='Exp. avg.',color='black',linewidth='1')
    #ax = plt.subplot(111)
    #ax.grid()


    #p3.line(x=kWhPerDay.index.values,y=kWhPerDay,legend='I '+str(inverterID)+': inverterName')

    list = []
    for inverter in project.inverters:
        list.append(inverter[1].kWP)

    minkWP=min(list)
    dfMaxkWh=(kWhPerDay/minkWP).max().max()
    p3.y_range=Range1d(-0.5, 1.2*dfMaxkWh)
    ax.set_ylim([-0.5, 1.2*dfMaxkWh])


    legend2 = Legend(items=plotlines,location=(55, 0)) #-30
    p3.add_layout(legend2, 'above')
    p3.legend.click_policy="hide"
    p3.legend.orientation = "horizontal"



    ax.set_xticks(plotDates[0::1],minor=False)
    ax.set_xticks(plotDates[1::2],minor=True)

    ax.set_xticklabels(plotDates,rotation=45,ha='right',fontsize=8)
    ax.xaxis.grid(linewidth=0.5,which='minor')
    ax.yaxis.grid(linewidth=0.5,which='major')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=8, fancybox=True)
    myFmt = mdates.DateFormatter('%d %B %Y')
    ax.xaxis.set_major_formatter(myFmt)

    fig.savefig(tempPlotDir+'plot1.png', bbox_inches='tight')


    p3.xaxis[0].ticker=DatetimeTicker(desired_num_ticks=len(kWhPerDay))

    leftlist = []
    rightlist = []
    info2div = createInfoTitle('Inverter: overview kWh/kWP')
    inverterID2=0
    inverterLayout = []
    for inverterName in kWhPerDay.columns.values:
        totalGenerated = kWhPerDay[kWhPerDay.columns[inverterID2]].sum()
        inverter = project.getInverter(inverterID2)
        realDailyAvg=round(totalGenerated/inverter.kWP/len(kWhPerDay.index.values),2)
        GIIdaily= project.getGII(projectDateBeginString,projectDateEndString)

        expPR=round(project.getExpectedPR(projectDateBeginString,projectDateEndString),1)
        expDailyAvg=round(expPR*GIIdaily/100,2)



        PR=round(realDailyAvg/GIIdaily*100,1)



        #PR = round((totalGenerated/project.invertersTotKWP[inverterID2])/InplaneProduction,3)*100

        printObject.invertersPR.append(str(PR))
        printObject.invertersTotalGenerated.append(str(int(round(totalGenerated))))
        printObject.invertersRealDailyAvgKWP.append(str(realDailyAvg))
        printObject.invertersExpDailyAvgKWP.append(str(expDailyAvg))


        leftlist = [('Real performance ratio',str(PR)+'%'),('Real total production',str(int(round(totalGenerated)))+' kWh'),
                     ('Real daily average',str(realDailyAvg)+' kWh/kWP'),('Real daily average',str(realDailyAvg*inverter.kWP)+' kWh')]

        rightlist=[('Inverter type',str(inverter.type)),('Installed capacity',str(inverter.kWP)+' kWP'),('Nominal installed capacity',str(inverter.kW)+' kW'),
                   ('Expected daily average',str(expDailyAvg)+' kWh/kWP'),('Expected daily average',str(round((expDailyAvg*inverter.kW),2))+' kWh')]

        inverterLayout.append(createInfoInverterPart(project,'inverter '+str(inverterID2+1),'Performance indicators:',leftlist,'Inverter information:',rightlist))
        inverterID2+=1

    inverterLayout=column(inverterLayout)
    print(inverterLayout)
    inverterGraph=[info2div,p3,inverterLayout]

    return inverterGraph

def handlemakePDF(divPDF,project,projectDateBeginString,projectDateEndString,isTechReport,reportNumber,tempPlotDir,outputDirectory):
    divPDF.text ="""<p style="font-size:28px ;text-align: center">Creating PDF..."""
    #PM.makePDFReport(project,projectDateBeginString,projectDateEndString,isTechReport,reportNumber,tempPlotDir,outputDirectory)
    PM.testPDF2(tempPlotDir,project,reportNumber,projectDateBeginString,projectDateEndString,printObject,isTechReportRequest=isTechReport)
    divPDF.text ="""<p style="font-size:28px ;text-align: center">PDF created!"""

def createPDFButtonBanner(reportNumber,project,kWhPerDay,totalkWh,cloudData,rain,projectDateBeginString,projectDateEndString,tempPlotDir):
    outputDirectory =''
    buttonCreateExecReport = Button(label="Create executive report")
    buttonCreateTechnicalReport = Button(label="Create technical report")
    divPDF = Div(text="""<p style="font-size:28px ;text-align: center">Solcor""",
    width=600, height=100)
    buttonCreateExecReport.on_click(partial(handlemakePDF,divPDF,project,projectDateBeginString,projectDateEndString,False,reportNumber,tempPlotDir,outputDirectory))
    buttonCreateTechnicalReport.on_click(partial(handlemakePDF,divPDF,project,projectDateBeginString,projectDateEndString,True,reportNumber,tempPlotDir,outputDirectory))



    buttonBanner = row([buttonCreateExecReport,divPDF,buttonCreateTechnicalReport])

    return buttonBanner

def showProjectScreen(reportNumber,project,kWhPerDay,totalkWh,cloudData,rain,projectDateBeginString,projectDateEndString):

        buttonBanner = createPDFButtonBanner(reportNumber,project,kWhPerDay,totalkWh,cloudData,rain,projectDateBeginString,projectDateEndString,tempPlotDir)

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
        df = project.getAllInverterDatafromTo(projectDateBeginString,projectDateEndString)
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


        for inverter in project.getAllInverterDatafromTo(projectDateBeginString,projectDateEndString).columns:
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
        xcloud = cloudDataShiftIndex
        offset = 0
        ycloud= np.append(cloudData*0+1.1*dfMax+offset,[cloudData[0]*0+1.1*dfMax+offset])
        namesCloud= ['cloud']+meansLabel
        source = ColumnDataSource(data=dict(x=cloudDataShiftIndex,
                                    y=np.append(cloudData*0+dfMax,[cloudData[0]*0+dfMax]),
                                    names=['cloud']+meansLabel))



        cloudLabels = LabelSet(x='x', y='y', text='names', level='glyph',x_offset=-5, y_offset=17,source=source, render_mode='canvas',text_font_size="10pt",text_color='grey')
        p.add_layout(cloudLabels)
        i=0
        for (a,b,c) in zip(xcloud,ycloud,namesCloud):
            if (i == 0):
                ax1.text(a,b,c, color='grey', horizontalalignment='left',fontsize=9)
            else:
                ax1.text(a,b,c, color='grey', horizontalalignment='center',fontsize=9)
            i+=1

#######ADD RAIN DATA

        amountOfRainDays = len([x for x in rain if x >= rainyDaythresholdPercentage])
        rainDataShiftIndex = rain.index + pd.DateOffset(hours=12)
        #l0 = p.circle(x=cloudData.index.values, y=cloudData*magnification, line_width=10,color='grey')
        rainLabel = [str(int(round(100*(x),0)))+'%' for x in rain.values.tolist()]


        beginLabelRain = rainDataShiftIndex.values[0] - np.timedelta64(1, 'D')
        #rainDataShiftIndex = np.insert(rainDataShiftIndex,0,beginLabelRain)
        rainDataShiftIndex = np.r_[beginLabelRain, rainDataShiftIndex]
        offset=0
        x=rainDataShiftIndex
        y=np.append(rain*0+1.2*dfMax+offset,[rain[0]*0+1.2*dfMax+offset])
        names=['Rain']+rainLabel
        rainSource = ColumnDataSource(data=dict(x=rainDataShiftIndex,
                                    y=np.append(rain*0+dfMax,[rain[0]*0+dfMax]),
                                    names=['Rain']+rainLabel))

        rainLabels = LabelSet(x='x', y='y', text='names', level='glyph',x_offset=-5, y_offset=30,source=rainSource, render_mode='canvas',text_font_size="10pt",text_color='blue')
        p.add_layout(rainLabels)
        i=0
        for (a,b,c) in zip(x,y,names):
            if (i == 0):
                ax1.text(a,b,c, color='blue', horizontalalignment='left',fontsize=9)
            else:
                ax1.text(a,b,c, color='blue', horizontalalignment='center',fontsize=9)
            i+=1



######fill info banner
        leftlist = [('Number of cloudy days',amountOfCloudDays),('Number of rainy days',amountOfRainDays)]
        printObject.nrOfCloudyDays=amountOfCloudDays
        printObject.nrOfRainyDays=amountOfRainDays

        cleaningDatesString=[createReadableDate(str(cleaning.date()))[0:5] for cleaning in project.cleaningDates]
        internetProbString = [createReadableDate(str(internetProb.date()))[0:5] for internetProb in project.internetProblems]
        gridProbString = [createReadableDate(str(gridProb.date()))[0:5] for gridProb in project.gridProblemData]
        maintenaceString = [createReadableDate(str(maintenace.date()))[0:5] for maintenace in project.maintenanceData]
        extraCommentString = [str(comment) for comment in project.commentList]
        extraCommentString=" ".join(extraCommentString)
        extraCommentString=re.sub("(.{80})", "\\1\n", extraCommentString, 0, re.DOTALL)


        printObject.cleaningDatestring=cleaningDatesString
        printObject.internetProbString=internetProbString
        printObject.gridProbString=gridProbString
        printObject.maintenaceString=maintenaceString
        printObject.extraCommentString=extraCommentString

        rightlist = [('Cleaning dates',str(cleaningDatesString)),('Internet problems dates',str(internetProbString)),
                     ('Grid Problems dates',str(gridProbString)),('Maintenance dates',str(maintenaceString)),('Comment',str(extraCommentString))]
        titleDiv = createInfoTitle('Global overview kW')
        inf = createInfoPart(project,'Weather information:',leftlist,'Maintenance information:',rightlist)


####ADD clean DATA
        NrOfDates = len(project.cleaningDates)
        shiftedCleaningDates = [x+pd.DateOffset(hours=12) for x in project.cleaningDates]
        cleaningLabels = p.circle(x=shiftedCleaningDates,y=[1.03*dfMax]*NrOfDates,line_color='orange',line_width=10)
        lineLegends.append(('cleaning',[cleaningLabels]))

        ax1.scatter(shiftedCleaningDates,[1.03*dfMax]*NrOfDates,color='orange',label='cleaning',s=30)


        NrOfDatesG = len(project.gridProblemData)
        shiftedGridProbDates = [x+pd.DateOffset(hours=12) for x in project.gridProblemData]
        gribProdLabels = p.circle(x=shiftedGridProbDates,y=[1.03*dfMax]*NrOfDatesG,line_color='red',line_width=10)

        ax1.scatter(shiftedGridProbDates,[1.03*dfMax]*NrOfDatesG,color='red',label='Problem',s=30)


        NrOfDatesM = len(project.maintenanceData)
        shiftedmaintanenanceDates = [x+pd.DateOffset(hours=12) for x in project.maintenanceData]
        maintenanceLabels = p.circle(x=shiftedmaintanenanceDates,y=[1.03*dfMax]*NrOfDatesM,line_color='red',line_width=10)

        ax1.scatter(shiftedmaintanenanceDates,[1.03*dfMax]*NrOfDatesM,color='red',s=30)

        NrOfDatesI = len(project.internetProblems)
        shiftedinternetProbDates = [x+pd.DateOffset(hours=12) for x in project.internetProblems]
        internetProbLabels = p.circle(x=shiftedinternetProbDates,y=[1.03*dfMax]*NrOfDatesI,line_color='red',line_width=10)
        lineLegends.append(('Problem',[gribProdLabels,maintenanceLabels,internetProbLabels]))

        ax1.scatter(shiftedinternetProbDates,[1.03*dfMax]*NrOfDatesI,color='red',s=30)



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


        ax1.set_ylim([-0.5, 1.3*dfMax])
        ax1.set_xticks(plotDates2[0::1],minor=False)
        ax1.set_xticks(plotDates2[1::2],minor=True)
        ax1.set_xticklabels(plotDates2,rotation=45,ha='right',fontsize=8)
        ax1.xaxis.grid(linewidth=0.5,which='minor')
        ax1.yaxis.grid(linewidth=0.5,which='major')
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
              ncol=8, fancybox=True)
        myFmt = mdates.DateFormatter('%d %B %Y')
        ax1.xaxis.set_major_formatter(myFmt)

        fig3.savefig(tempPlotDir+'plot3.png', bbox_inches='tight')



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




        ###ADD Averages

        expPR=round(project.getExpectedPR(projectDateBeginString,projectDateEndString),1)
        GIIdaily=project.getGII(projectDateBeginString,projectDateEndString)
        projectAVG = round(expPR*GIIdaily/100,2)
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
        ax1.set_xticks(plotDates2[0::1],minor=False)
        ax1.set_xticks(plotDates2[1::2],minor=True)
        ax1.set_xticklabels(plotDates,rotation=45,ha='right',fontsize=8)
        ax1.xaxis.grid(linewidth=0.5,which='minor')
        ax1.yaxis.grid(linewidth=0.5,which='major')
        ax1.legend(h1+h2, l1+l2,loc='upper center', bbox_to_anchor=(0.5, 1.1),
              ncol=8, fancybox=True)
        myFmt = mdates.DateFormatter('%d %B %Y')
        ax1.xaxis.set_major_formatter(myFmt)

        fig2.savefig(tempPlotDir+'plot2.png', bbox_inches='tight')

        #BIO.output_file(filename='p2.html',mode='inline')

        #BIO.show(curdoc(), new='tab', notebook_handle=False, notebook_url='localhost:8888')

        #file = BIO.save(p2)
        #print(file)

        ###Performance indicators

        totalGenerated = totalkWh


        underperfDays = sum([1 if x<projectAVG*project.totalkWP else 0 for x in totalKWhPerday[totalKWhPerday.columns[0]]])
        overperfDays = sum([1 if x>=projectAVG*project.totalkWP else 0 for x in totalKWhPerday[totalKWhPerday.columns[0]]])



        GHIdaily= project.getGHI(projectDateBeginString,projectDateEndString)
        GIIdaily= project.getGII(projectDateBeginString,projectDateEndString)
        percentage = round(project.getPercentageChange(projectDateBeginString,projectDateEndString),2)

        expPR=round(project.getExpectedPR(projectDateBeginString,projectDateEndString),1)
        expDailyAvg=round(expPR*GIIdaily/100,2)




        realDailyAvg=round((totalGenerated/project.totalkWP/len(df.index.values)),2)
        PR=round(realDailyAvg/GIIdaily*100,1)
        #PR = round((totalGenerated/project.totalkWP)/InplaneProduction,3)*100
        print('PR:'+str(PR))

        printObject.totPR=PR
        printObject.totalGenerated=totalGenerated
        printObject.totRealDailyAvg = realDailyAvg
        printObject.GHIdaily=GHIdaily
        printObject.GIIdaily=GIIdaily

        printObject.expPR=expPR
        printObject.expDailyAvg=expDailyAvg
        printObject.totalKWhPerday=totalKWhPerday
        printObject.realDailyAvg=realDailyAvg
        printObject.underperfDays=underperfDays
        printObject.overperfDays=overperfDays





        leftlist = [('Real performance ratio',str(PR)+'%'),('GHI daily',str(GHIdaily)+' kWh/m^2'),('GII daily',str(GIIdaily)+' kWh/m^2'),('Real total production',str(round(totalGenerated,2))+' kWh'),
                     ('Real daily average',str(realDailyAvg)+' kWh/kWP'),('Real daily average',str(realDailyAvg*project.totalkWP)+' kWh')]
        rightlist = [('Expected performance ratio',str(expPR)+ '%'),('Expected daily average',str(expDailyAvg)+' kWh/kWP'),
                     ('Expected daily average',str(round((expDailyAvg*project.totalkWP),2))+' kWh'),('Expected monthly production',str(round((expDailyAvg*project.totalkWP*len(totalKWhPerday)),2))+' kWh'),('Number of underperforming days',underperfDays),('Number of overperforming days',overperfDays)]
        titDiv = createInfoTitle('Global overview kWh & kWh/kWP')
        info2div = createInfoPart(project,'Real performance indicators:',leftlist,'Estimated performance indicators:',rightlist)

        GlobalKwhGraph=column([titDiv,p2,info2div])

#########INVERTERGRAPH



        inverterGraphs =[]
        inverterGraphs.append(createInverterPlots(kWhPerDay,project,projectDateBeginString,projectDateEndString))

        inverterGraphs= [item for sublist in inverterGraphs for item in sublist]
        inverterGraphs = column(inverterGraphs)

        globalLayout = column([buttonBanner,globalkWGraph,GlobalKwhGraph,inverterGraphs])

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
    totalData = [str(x.value) for x in [total,totalkw,totExtra]]
    #inverter1Data =[str(x.value) for x in [inverter1Type,inverter1Tot,inverter1Totkw,inverter1Extra,filePick1,fileColumn1] ]
    #inverter2Data = [str(x.value) for x in [inverter2Type,inverter2Tot,inverter2Totkw,inveter2Extra,filePick2,fileColumn2]]


    InverterData=[]
    for inverter in inverterLabels:
        InverterData.append([str(x.value) for x in inverter])


    #InverterData = [inverter1Data,inverter2Data]
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
    projectDateBeginString = datetime.datetime.strptime(projectDateBeginString, '%d-%m-%Y %H:%M:%S')
    projectDateBeginString = projectDateBeginString.strftime("%Y-%m-%d %H:%M:%S")

    projectDateEndString =str(projectDateEnd.value)
    projectDateEndString = datetime.datetime.strptime(projectDateEndString, '%d-%m-%Y %H:%M:%S')
    projectDateEndString = projectDateEndString.strftime("%Y-%m-%d %H:%M:%S")

    ExtraData = str(extraComments.value)
    reportNumber = str(reportNumberTxt.value)
    GHIdf = CE.collectSolarisData(solargisLocation.value,str(projectDateBegin.value)[6:10])



    project = PE.createProject(generalData,geoData,totalData,InverterData,maintancelist ,ExtraData,adresData,GHIdf,str(sampleRate.value))
    inputData=(project.name,project.getAllInverterDatafromTo(projectDateBeginString,projectDateEndString))



    kWhPerDay = CE.getkWhPerDay(inputData,str(sampleRate.value))

    totalkWh = CE.getTotalkWh(inputData,str(sampleRate.value))







    cloudData = CE.returnAverageCloudData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)
    rain = CE.returnAverageRainData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)



    showProjectScreen(reportNumber,project,kWhPerDay,totalkWh,cloudData,rain,projectDateBeginString,projectDateEndString)


def insertInverterLayout():
    global inverterClickCounter
    global inverterLabels
    global globNewLayout
    global newLayout
    oldLayout=newLayout
    inverterID = inverterClickCounter+2
    inverterXType = TextInput(value="20000TL-30", title="Inverter "+str(inverterID)+" type:")


    inverterXTotKWP = TextInput(value="20,5", title="Inverter X"+str(inverterID)+" installed cap xx[kWP]:")
    inverterXTotKW = TextInput(value="20", title="Inverter X"+str(inverterID)+" installed cap xx[kW]:")
    #inverter1Avg = TextInput(value="4.87", title="Inverter x exp. daily avg. [kWh/KWP]:")
    inverterXExtra = TextInput(value="", title="InverterX "+str(inverterID)+" EXTRA:")

    filePickX = TextInput(value="/Users/christiaan/Desktop/Solcor/dataMergeWeek/Neuces2/Nueces/Nueces", title="Inverter "+str(inverterID)+" data:")
    fileColumnX = TextInput(value="1", title="InverterX "+str(inverterID)+" column nr in file:")

    inverterXRow1= [inverterXType,filePickX,fileColumnX]
    inverterXRow2= [inverterXTotKWP,inverterXTotKW,inverterXExtra]

    divX = [Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)]


    oldLayout.insert(12+3*inverterClickCounter,inverterXRow1)
    oldLayout.insert(13+3*inverterClickCounter,inverterXRow2)
    oldLayout.insert(14+3*inverterClickCounter,divX)


    updatedLayout = oldLayout[:]
    globNewLayout.children = []
    globNewLayout.children=[layout(updatedLayout)]

    inverterClickCounter+=1

    inverterLabels.append([inverterXType,inverterXTotKWP,inverterXTotKW,inverterXExtra,filePickX,fileColumnX])




def createNewProjectScreen(quickReport=False):
    global inverterClickCounter
    inverterClickCounter=0
    global globNewLayout
    global newLayout
    global projectNameTxt,reportNumberTxt,projectOrientation,projectInclination,projectLatitude,projectLongitude,projectDateBegin,projectDateEnd,total,totalkw,totAvg,totExtra
    global projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt,sampleRate
    global inverter1Type,inverter1Tot,inverter1Totkw,inverter1Extra,filePick1,inverter2Type,inverter2Tot,inverter2Totkw,inveter2Extra,filePick2
    global cleaningDate,extraComments,structureDD,gridProbDate,maintenanceDate,internetProblemDate,solargisLocation
    div0 = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)
    global fileColumn1,fileColumn2
    global inverterLabels
    inverterLabels=[]


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



    projectDateBegin = TextInput(value="01-04-2017 00:00:00", title="Begin date report:")
    projectDateEnd = TextInput(value="30-04-2017 23:45:00", title="End date report:")

    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    total = TextInput(value="46", title="Total installed cap [kWP]:")
    totalkw = TextInput(value="45", title="Total installed cap [kW]:")
    sampleRate = TextInput(value="15Min", title="Sample rate (e.g.'15Min','1H'):")
    totExtra = TextInput(value="", title="Total Extra:")


    div2 = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    inverter1Type = TextInput(value="25000TL-30", title="Inverter 1 type:")


    inverter1Tot = TextInput(value="25,5", title="Inverter 1 installed cap [kWP]:")
    inverter1Totkw = TextInput(value="25", title="Inverter 1 installed cap [kW]:")
    #inverter1Avg = TextInput(value="4.87", title="Inverter 1 exp. daily avg. [kWh/KWP]:")
    inverter1Extra = TextInput(value="", title="Inverter 1 EXTRA:")

    filePick1 = TextInput(value="/Users/christiaan/Desktop/Solcor/dataMergeWeek/Neuces2/Nueces/Nueces", title="Inverter 1 data:")
    fileColumn1 = TextInput(value="2", title="Inverter 1 column nr in file:")


    inverterLabels.append([inverter1Type,inverter1Tot,inverter1Totkw,inverter1Extra,filePick1,fileColumn1])

    div3 = Div(text="""<hr noshade size=4 color=green>""",width=1000, height=30)


    cleaningDate = TextInput(value="", title="Cleaning date(s):")
    gridProbDate = TextInput(value="", title="Grid problem date(s):")
    maintenanceDate = TextInput(value="", title="Maintenance date(s):")
    internetProblemDate = TextInput(value="", title="Internet problem date(s):")





    extraComments = TextInput(value="Here is a comment...", title="Comments:")
    solargisLocation = TextInput(value='/Users/christiaan/Desktop/Solcor/dataMergeWeek/NDC_PV-8627-1705-1780_-31.783--70.984.xls', title="Solargis file location:")




    buttonBack = Button(label="Back")
    buttonBack.on_click(goToHomescreen)

    buttonAddInverter = Button(label="Add inverter")
    buttonAddInverter.on_click(partial(insertInverterLayout,))

    nextButton = None
    if quickReport:
        nextButton=Button(label='Next')
        nextButton.on_click(collectData)
    else:
        nextButton = Button(label='Add project')

    newLayout = [[projectNameTxt,reportNumberTxt],[projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt],[div0],[projectLatitude,projectLongitude,structureDD],[projectOrientation,projectInclination,projectDateBegin,projectDateEnd],[],
                 [div],[total,totalkw,sampleRate,totExtra],[div2],[inverter1Type,filePick1,fileColumn1],[inverter1Tot,inverter1Totkw,inverter1Extra],
                 [div3],[cleaningDate,gridProbDate,maintenanceDate,internetProblemDate],[extraComments,solargisLocation],[nextButton,buttonBack,buttonAddInverter]]


    globNewLayout.children = []
    globNewLayout.children=[layout(newLayout)]
    #insertInverterLayout(newLayout)
    #print('lenupdate',len(upDatedLayout))

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






