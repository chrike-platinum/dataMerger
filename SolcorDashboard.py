# -*- coding: utf-8 -*-
__author__ = 'christiaan'

local_encoding = 'cp850'
tempPlotDir = 'tempPlots/'
plotFileName = 'plot'
global PDFoutput




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
import dataHandler as DH
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from inverter import Inverter


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
        lines =[line]
        if (len(kWhPerDay2.index.values)==1):
            linePoint = p3.circle(x=kWhPerDay2.index.values,y=kWhPerDay2,color=color, size=10)
            lines.append(linePoint)
        plotlines.append(('Inv '+str(inverterID+1),lines))
        plotDates = [createReadableDate(date) for date in kWhPerDay2.index.values]
        plotDates = [datetime.datetime.strptime(d,'%d/%m/%Y').date() for d in plotDates]
        if (len(kWhPerDay2.index.values)==1):
            ax.plot(plotDates,kWhPerDay2,label='Inv '+str(inverterID),color=color,marker='o',linewidth='1')
        else:
            ax.plot(plotDates,kWhPerDay2,label='Inv '+str(inverterID),color=color,linewidth='1')
        inverterID +=1


    GIIdaily= project.getGII(projectDateBeginString,projectDateEndString)

    expPR=round(project.getExpectedPR(projectDateBeginString,projectDateEndString),1)
    expDailyAvg=round(expPR*GIIdaily/100,2)

    avg = [expDailyAvg]*len(kWhPerDay.index.values)
    avgLine = p3.line(x=kWhPerDay2.index.values,y=avg,color='black')
    avgLines = [avgLine]
    if len(kWhPerDay2.index.values)==1:
        kwhLinePoints = p3.circle(x=kWhPerDay2.index.values,y=avg,color='black', size=10)
        ax.plot(plotDates,avg,label='Exp. avg.',color='black',marker='o',linewidth='1')
        avgLines.append(kwhLinePoints)
    else:
        ax.plot(plotDates,avg,label='Exp. avg.',color='black',linewidth='1')
    plotlines.append(('Exp. avg.',avgLines))



    #ax = plt.subplot(111)
    #ax.grid()


    #p3.line(x=kWhPerDay.index.values,y=kWhPerDay,legend='I '+str(inverterID)+': inverterName')

    list = []
    for inverter in project.inverters:
        list.append(inverter[1].kWP)

    minkWP=min(list)
    dfMaxkWh=(kWhPerDay/minkWP).max().max()
    dfMaxkWh=max(expDailyAvg,dfMaxkWh)

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

        plotDates = [date for date in df.index.values]
        plotDates = [date for date in plotDates]# if (pd.Timestamp(date).time().strftime('%H:%M:%S')=='00:00:00')]
        plotDates2 = [date for date in plotDates if (pd.Timestamp(date).time().strftime('%H:%M:%S')=='00:00:00')]
        #plotDates = [datetime.datetime.strptime(d,'%d/%m/%Y %H:%m:%S').date() for d in plotDates]
        #plotDates = [createReadableDate(date) for date in plotDates]

        inverterID3=0
        for inverter in project.getAllInverterDatafromTo(projectDateBeginString,projectDateEndString).columns:
            color = next(colorPool)
            line = p.line(x=df.index.values,y=df[inverter],color=color)
            ax1.plot(plotDates,df[inverter],label='Inv '+str(inverterID3),color=color,linewidth='1')
            inverterID3+=1
            lineLegends.append(('Inv '+str(inverterID3),[line]))


        #hp = Horizon(df,plot_width=800, plot_height=500,
        #     title="horizon plot using stock inputs")


#####ADD Cloud DATA
        amountOfCloudDays = len([x for x in cloudData if float(x*100) >= cloudyDaythresholdPercentage])
        cloudDataShiftIndex = cloudData.index + pd.DateOffset(hours=12)

        #l0 = p.circle(x=cloudData.index.values, y=cloudData*magnification, line_width=10,color='grey')
        meansLabel = [str(int(round(100*(x),0)))+'%' for x in cloudData.values.tolist()]

        if len(cloudDataShiftIndex)>=10:
            beginLabelCloud = cloudDataShiftIndex.values[0] - np.timedelta64(24, 'h')
        else:
            beginLabelCloud = cloudDataShiftIndex.values[0] - np.timedelta64(12, 'h')
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
        amountOfRainDays = len([x for x in rain if float(x*100) >= rainyDaythresholdPercentage])
        rainDataShiftIndex = rain.index + pd.DateOffset(hours=12)
        #l0 = p.circle(x=cloudData.index.values, y=cloudData*magnification, line_width=10,color='grey')
        rainLabel = [str(int(round(100*(x),0)))+'%' for x in rain.values.tolist()]

        if len(rainDataShiftIndex)>=10:
            beginLabelRain = rainDataShiftIndex.values[0] - np.timedelta64(24, 'h')
        else:
            beginLabelRain = rainDataShiftIndex.values[0] - np.timedelta64(12, 'h')
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
        leftlist = [('Number of rainy days',amountOfRainDays),('Number of cloudy days',amountOfCloudDays)]
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
        beginDate = totalKWhPerday.index.values[0]
        endDate = totalKWhPerday.index.values[-1]
        idx = pd.date_range(beginDate, endDate)
        totalKWhPerday = totalKWhPerday.to_frame().reindex(idx, fill_value=0)
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
        if len(df.index.values)==1:
            ax1.plot(plotDates,yValues,label='kWh',color='blue',marker='o',linewidth='1')
        else:
            ax1.plot(plotDates,yValues,label='kWh',color='blue',linewidth='1')

        p2.yaxis.axis_label_text_color = "blue"
        p2.add_layout(LinearAxis(y_range_name="etxraAxis",axis_label='kWh/kWP',axis_label_text_color='green'), 'right')

        p2.xaxis[0].ticker=DatetimeTicker(desired_num_ticks=len(cloudData))




        ###ADD Averages

        expPR=round(project.getExpectedPR(projectDateBeginString,projectDateEndString),1)
        GIIdaily=project.getGII(projectDateBeginString,projectDateEndString)
        projectAVG = round(expPR*GIIdaily/100,2)
        dfMaxkWh=max(projectAVG*project.totalkWP,dfMaxkWh)

        p2.y_range=Range1d(-0.5, 1.2*dfMaxkWh)


        yvaluesAVG = [projectAVG*project.totalkWP]*len(yValues)
        ExpAvhKwhLine = p2.line(x=df.index.values,y=yvaluesAVG,color='lightblue',line_width=2)
        kwhKWPLIne = p2.line(x=df.index.values,y=yValues/project.totalkWP,color='green',y_range_name="etxraAxis")


        if len(plotDates)==1:
            ax2.plot(plotDates,yValues/project.totalkWP,label='kWh/kWP',color='green',marker='o',linewidth='1')
            ax1.plot(plotDates,yvaluesAVG,label='Exp. Avg. kWh',color='lightblue',marker='o',linewidth='1')
        else:
            ax2.plot(plotDates,yValues/project.totalkWP,label='kWh/kWP',color='green',linewidth='1')
            ax1.plot(plotDates,yvaluesAVG,label='Exp. Avg. kWh',color='lightblue',linewidth='1')


        yValueskWP=[projectAVG]*len(yValues)#[x/project.totalkWP for x in yvaluesAVG]
        dfMaxkWhkWP=max(dfMaxkWhkWP,projectAVG)

        p2.extra_y_ranges = {"etxraAxis": Range1d(start=0, end=2*dfMaxkWhkWP)}
        ExpKWhKWP= p2.line(x=df.index.values,y=yValueskWP,y_range_name="etxraAxis",color='lightgreen',line_width=2)
        if(len(plotDates)==1):
            ax2.plot(plotDates,yValueskWP,label='Exp. Avg. kWh/kWP',color='lightgreen',marker='o',linewidth='1')
        else:
            ax2.plot(plotDates,yValueskWP,label='Exp. Avg. kWh/kWP',color='lightgreen',linewidth='1')


        if (len(df.index.values)==1):
            ExpKWhKWPLinePoints = p2.circle(x=df.index.values,y=yValueskWP,y_range_name="etxraAxis",color='lightgreen', size=10)
            kwhLinePoints = p2.circle(x=df.index.values,y=yValues,color='blue', size=10)
            ExpAvhKwhLinePoints = p2.circle(x=df.index.values,y=yvaluesAVG,color='lightblue', size=10)
            kwhKWPLinePoints = p2.circle(x=df.index.values,y=yValues/project.totalkWP,y_range_name="etxraAxis",color='green', size=10)

            lineLegends2.append(('kWh',[kwhLine,kwhLinePoints]))
            lineLegends2.append(('Exp. Avg. kWh',[ExpAvhKwhLine,ExpAvhKwhLinePoints]))
            lineLegends2.append(('kWh/kWP',[kwhKWPLIne,kwhKWPLinePoints]))
            lineLegends2.append(('Exp. Avg. kWh/kWP',[ExpKWhKWP,ExpKWhKWPLinePoints]))
        else:
            lineLegends2.append(('kWh',[kwhLine]))
            lineLegends2.append(('Exp. Avg. kWh',[ExpAvhKwhLine]))
            lineLegends2.append(('kWh/kWP',[kwhKWPLIne]))
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

        beginDate = kWhPerDay.index.values[0]
        endDate = kWhPerDay.index.values[-1]
        idx = pd.date_range(beginDate, endDate)
        kWhPerDay = kWhPerDay.reindex(idx, fill_value=0)

        inverterGraphs =[]
        inverterGraphs.append(createInverterPlots(kWhPerDay,project,projectDateBeginString,projectDateEndString))

        inverterGraphs= [item for sublist in inverterGraphs for item in sublist]
        inverterGraphs = column(inverterGraphs)

        buttonBack = Button(label="Back")
        buttonBack.on_click(goToHomescreen)

        globalLayout = column([buttonBanner,globalkWGraph,GlobalKwhGraph,inverterGraphs,buttonBack])

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




def collectData(statusBanner,saveData=False):

    projectsInDB = DH.getListOfProjectNames()
    if ((not (projectNameTxt.value.lower() in projectsInDB) and saveData==True) or saveData==False):

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

        extraCommentsDateString = str(extraCommentsDate.value)
        extraCommentsDateString = datetime.datetime.strptime(extraCommentsDateString, '%d-%m-%Y')
        extraCommentsDateString = extraCommentsDateString.strftime("%d-%m-%Y")


        ExtraData = (extraCommentsDateString,str(extraCommentX.value))
        reportNumber = str(reportNumberTxt.value)
        GHIdf = CE.collectSolarisData(solargisLocation.value,str(solargisYear.value))



        project = PE.createProject(generalData,geoData,totalData,InverterData,maintancelist,ExtraData,adresData,solargisLocation.value,GHIdf)
        if (saveData==True):
            print('Saving project to database...')
            DH.saveProject(project)
            statusBanner.text="Project saved!"
        else:
            inputData=(project.name,project.getAllInverterDatafromTo(projectDateBeginString,projectDateEndString))
            kWhPerDay = CE.getkWhPerDay(inputData,[x[6] for x in InverterData])
            totalkWh = CE.getTotalkWh(inputData,[x[6] for x in InverterData])


            cloudData = CE.returnAverageCloudData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)
            rain = CE.returnAverageRainData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)
            showProjectScreen(reportNumber,project,kWhPerDay,totalkWh,cloudData,rain,projectDateBeginString,projectDateEndString)
    else:
        statusBanner.text="Error: Project name already in Database!"


def insertInverterLayout():
    global inverterClickCounter
    global inverterLabels
    global globNewLayout
    global newLayout
    oldLayout=newLayout
    inverterID = inverterClickCounter+2
    inverterXType = TextInput(value="20000TL-30", title="Inverter "+str(inverterID)+" type:")


    inverterXTotKWP = TextInput(value="20,5", title="Inverter "+str(inverterID)+" installed cap [kWP]:")
    inverterXTotKW = TextInput(value="20", title="Inverter "+str(inverterID)+" installed cap [kW]:")
    #inverter1Avg = TextInput(value="4.87", title="Inverter x exp. daily avg. [kWh/KWP]:")
    inverterXExtra = TextInput(value="", title="Inverter "+str(inverterID)+" EXTRA:")
    inverterXSampleRate = TextInput(value="15Min", title="Sample rate (e.g.'15Min','1H'):")


    filePickX = TextInput(value="/Users/christiaan/Desktop/Solcor/dataMergeWeek/Neuces2/Nueces/Nueces", title="Inverter "+str(inverterID)+" data:")
    fileColumnX = TextInput(value="1", title="Inverter "+str(inverterID)+" column nr in file:")

    inverterXRow1= [inverterXType,filePickX,fileColumnX,inverterXSampleRate]
    inverterXRow2= [inverterXTotKWP,inverterXTotKW,inverterXExtra]


    divX = [Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)]

    oldLayout.insert(13+3*inverterClickCounter,divX)
    oldLayout.insert(14+3*inverterClickCounter,inverterXRow1)
    oldLayout.insert(15+3*inverterClickCounter,inverterXRow2)



    updatedLayout = oldLayout[:]
    globNewLayout.children = []
    globNewLayout.children=[layout(updatedLayout)]

    inverterClickCounter+=1


    inverterLabels.append([inverterXType,inverterXTotKWP,inverterXTotKW,inverterXExtra,filePickX,fileColumnX,inverterXSampleRate])

def removeInverterLayout():
    global inverterClickCounter
    global inverterLabels
    global globNewLayout
    global newLayout
    oldLayout=newLayout

    if inverterClickCounter !=0:

        inverterClickCounter-=1
        print('counter',inverterClickCounter)

        del oldLayout[13+3*inverterClickCounter]
        del oldLayout[13+3*inverterClickCounter]
        del oldLayout[13+3*inverterClickCounter]


        updatedLayout = oldLayout[:]
        globNewLayout.children = []
        globNewLayout.children=[layout(updatedLayout)]



def createNewProjectScreen(quickReport=False):
    global inverterClickCounter
    inverterClickCounter=0
    global globNewLayout
    global newLayout
    global projectNameTxt,reportNumberTxt,projectOrientation,projectInclination,projectLatitude,projectLongitude,projectDateBegin,projectDateEnd,total,totalkw,totAvg,totExtra
    global projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt,inverter1SampleRate
    global inverter1Type,inverter1Tot,inverter1Totkw,inverter1Extra,filePick1,inverter2Type,inverter2Tot,inverter2Totkw,inveter2Extra,filePick2
    global cleaningDate,extraCommentX,structureDD,gridProbDate,maintenanceDate,internetProblemDate,solargisLocation,solargisYear,extraCommentsDate
    div0 = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)
    global fileColumn1,fileColumn2
    global inverterLabels
    inverterLabels=[]

    if (quickReport):
        title="Create quick report"
    else:
        title="Add new project"
    headingTxt = Div(text="""<p style="font-size:20px;text-align: center">"""+title,
            width=1200, height=30)

    headingDiv = Div(text="""<hr noshade size=4 color=green>""",
        width=1200, height=30)


    projectNameTxt = TextInput(value="Nueces Del Choapa", title="Project name:")
    reportNumberTxt= TextInput(value="1", title="Report number:")

    projectContactTxt = TextInput(value="Leonardo Pasten", title="Contact person:")
    projectStreetTxt = TextInput(value="Principal el Tambo", title="Street + nr:")
    projectCityTxt = TextInput(value="Salamanca Chile", title="City (+ Country):")
    projectTelephoneTxt = TextInput(value="", title="Telephone:")

    div0 = Div(text="""<hr noshade size=4 color=green>""",
        width=1100, height=30)

    projectOrientation =TextInput(value="-10", title="Project orientation:")
    projectInclination = TextInput(value="15", title="Project inclination:")
    projectLatitude = TextInput(value="""31° 46' 59.27" S""", title="Project latitude:")
    projectLongitude = TextInput(value="""70° 59' 3.36" W""", title="Project longitude:")




    structureDD = Select(title='Structure', value='Parallel to roof', options=["Parallel to roof","Structure with inclination"])


    if (quickReport):
        projectDateBegin = TextInput(value="01-04-2017 00:00:00", title="Begin date report:")
        projectDateEnd = TextInput(value="30-04-2017 23:45:00", title="End date report:")



    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1100, height=30)


    total = TextInput(value="46", title="Total installed cap [kWP]:")
    totalkw = TextInput(value="45", title="Total installed cap [kW]:")
    totExtra = TextInput(value="", title="Total Extra:")


    div2 = Div(text="""<hr noshade size=4 color=green>""",
        width=1100, height=30)


    inverter1Type = TextInput(value="25000TL-30", title="Inverter 1 type:")


    inverter1Tot = TextInput(value="25,5", title="Inverter 1 installed cap [kWP]:")
    inverter1Totkw = TextInput(value="25", title="Inverter 1 installed cap [kW]:")
    #inverter1Avg = TextInput(value="4.87", title="Inverter 1 exp. daily avg. [kWh/KWP]:")
    inverter1Extra = TextInput(value="", title="Inverter 1 EXTRA:")
    inverter1SampleRate = TextInput(value="15Min", title="Sample rate (e.g.'15Min','1H'):")

    filePick1 = TextInput(value="/Users/christiaan/Desktop/Solcor/dataMergeWeek/Neuces2/Nueces/Nueces", title="Inverter 1 data:")
    fileColumn1 = TextInput(value="2", title="Inverter 1 column nr in file:")


    inverterLabels.append([inverter1Type,inverter1Tot,inverter1Totkw,inverter1Extra,filePick1,fileColumn1,inverter1SampleRate])

    div3 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)


    cleaningDate = TextInput(value="", title="Cleaning date(s):")
    gridProbDate = TextInput(value="", title="Grid problem date(s):")
    maintenanceDate = TextInput(value="", title="Maintenance date(s):")
    internetProblemDate = TextInput(value="", title="Internet problem date(s):")


    extraCommentX = TextInput(value="Here is a comment...", title="Comment:")
    extraCommentsDate=TextInput(value="10-04-2017", title="Date comment:")
    solargisLocation = TextInput(value='/Users/christiaan/Desktop/Solcor/dataMergeWeek/NDC_PV-8627-1705-1780_-31.783--70.984.xls', title="Solargis file location:")
    solargisYear = TextInput(value='2017', title="Solargis file year:")


    div4 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)

    buttonBack = Button(label="Back")
    buttonBack.on_click(goToHomescreen)

    buttonAddInverter = Button(label="Add inverter")
    buttonAddInverter.on_click(partial(insertInverterLayout,))

    buttonRemoveInverter = Button(label="Remove inverter")
    buttonRemoveInverter.on_click(partial(removeInverterLayout,))

    statusBanner=Div(text="""<p style="font-size:14px ;text-align: center">""",
    width=600, height=100)

    nextButton = None
    if quickReport:
        nextButton=Button(label='Next')
        nextButton.on_click(partial(collectData,statusBanner))
    else:
        nextButton = Button(label='Add project')
        nextButton.on_click(partial(collectData,statusBanner,saveData=True))
    if (quickReport):
        newLayout = [[headingTxt],[headingDiv],[projectNameTxt,reportNumberTxt],[projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt],[div0],[projectLatitude,projectLongitude,structureDD],[projectOrientation,projectInclination,projectDateBegin,projectDateEnd],
                 [div],[total,totalkw,totExtra],[div2],[inverter1Type,filePick1,fileColumn1,inverter1SampleRate],[inverter1Tot,inverter1Totkw,inverter1Extra],
                 [],[buttonAddInverter,buttonRemoveInverter,div4],[cleaningDate,gridProbDate,maintenanceDate,internetProblemDate],[extraCommentX,extraCommentsDate,solargisLocation,solargisYear],[buttonBack,nextButton,statusBanner]]
    else:
        newLayout = [[headingTxt],[headingDiv],[projectNameTxt,reportNumberTxt],[projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt],[div0],[projectLatitude,projectLongitude,structureDD],[projectOrientation,projectInclination],
                 [div],[total,totalkw,totExtra],[div2],[inverter1Type,filePick1,fileColumn1,inverter1SampleRate],[inverter1Tot,inverter1Totkw,inverter1Extra],
                 [],[buttonAddInverter,buttonRemoveInverter,div4],[cleaningDate,gridProbDate,maintenanceDate,internetProblemDate],[extraCommentX,extraCommentsDate,solargisLocation,solargisYear],[buttonBack,nextButton,statusBanner]]


    globNewLayout.children = []
    globNewLayout.children=[layout(newLayout)]

#TODO
def collectInspectionData(project,projectDateBegin,projectDateEnd):
    projectDateBeginString = projectDateBegin.value
    projectDateEndString = projectDateEnd.value

    projectDateBeginString=str(projectDateBeginString)
    projectDateBeginString = datetime.datetime.strptime(projectDateBeginString, '%d-%m-%Y %H:%M:%S')
    projectDateBeginString = projectDateBeginString.strftime("%Y-%m-%d %H:%M:%S")

    projectDateEndString = projectDateEndString
    projectDateEndString = datetime.datetime.strptime(projectDateEndString, '%d-%m-%Y %H:%M:%S')
    projectDateEndString = projectDateEndString.strftime("%Y-%m-%d %H:%M:%S")


    inputData=(project.name,project.getAllInverterDatafromTo(projectDateBeginString,projectDateEndString))
    sampleRates=[]
    for inverterTuple in project.inverters:
        sampleRates.append(inverterTuple[1].sampleRate)


    kWhPerDay = CE.getkWhPerDay(inputData,sampleRates)
    totalkWh = CE.getTotalkWh(inputData,sampleRates)

    cloudData = CE.returnAverageCloudData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)
    rain = CE.returnAverageRainData(projectDateBeginString,projectDateEndString,project.projectLatitude,project.projectLongitude)
    showProjectScreen("Not assigned",project,kWhPerDay,totalkWh,cloudData,rain,projectDateBeginString,projectDateEndString)

def saveSelection(attr, old, new):
    global selection
    selection = new['1d']['indices']
def removeMaintenance(project,data_table):
    global selection
    dateToRemove = data_table.source.data['dates'][selection[0]]
    kindToRemove = data_table.source.data['maintenance'][selection[0]]


    if (kindToRemove == 'cleaning'):
        project.cleaningDates.remove(dateToRemove)
        print('done something to cleaning data')
    if kindToRemove == 'Grid problems':
        project.gridProblemData.remove(dateToRemove)
    if kindToRemove == 'Maintenance':
        project.maintenanceData.remove(dateToRemove)
    if kindToRemove == 'Internet problems':
        project.internetProblems.remove(dateToRemove)
    DH.saveProject(project)
    time.sleep(1)
    showManagementScreen('ID'+str(project.DBID))
def collectNewMaintanceData(project):
    cleaningData = cleaningDateX.value.split(',')
    cleaningData = [datetime.datetime.strptime(x, '%d-%m-%Y') for x in cleaningData if str(pd.to_datetime(x)) != 'NaT']

    gridProbData = gridProbDateX.value.split(',')
    gridProbData = [datetime.datetime.strptime(x, '%d-%m-%Y') for x in gridProbData if str(pd.to_datetime(x)) != 'NaT']

    maintanceData = maintenanceDateX.value.split(',')
    maintanceData = [datetime.datetime.strptime(x, '%d-%m-%Y') for x in maintanceData if str(pd.to_datetime(x)) != 'NaT']

    internetProbData = internetProblemDateX.value.split(',')
    internetProbData = [datetime.datetime.strptime(x, '%d-%m-%Y') for x in internetProbData if str(pd.to_datetime(x)) != 'NaT']

    for cleanNew in cleaningData:
        project.cleaningDates.append(cleanNew)
    for gridNew in gridProbData:
        project.gridProblemData.append(gridNew)
    for mainNew in maintanceData:
        project.maintenanceData.append(mainNew)
    for internetNew in internetProbData:
        project.internetProblems.append(internetNew)
    DH.saveProject(project)
    time.sleep(1)
    showManagementScreen('ID'+str(project.DBID))


def commentSelection(attr, old, new):
    global commentSelectionInt
    print(new['1d']['indices'])
    commentSelectionInt = new['1d']['indices']
def removeComment(project,data_table):
    global commentSelectionInt
    dateToRemove = data_table.source.data['dates'][commentSelectionInt[0]]
    commentToRemove = data_table.source.data['comment'][commentSelectionInt[0]]
    dateToRemove = dateToRemove.strftime("%d-%m-%Y")
    project.commentList.remove((dateToRemove,str(commentToRemove)))
    DH.saveProject(project)
    time.sleep(1)
    showManagementScreen('ID'+str(project.DBID))

def addComment(project):
    comment = extraCommentX.value
    date = extraCommentDateX.value
    project.commentList.append((date,comment))
    DH.saveProject(project)
    time.sleep(1)
    showManagementScreen('ID'+str(project.DBID))


def export(project):
    outputDir = str(outputDirectory.value)
    format = str(formatSelection.value)
    fileName=str(outputDir+'/'+str(project.name)+' consumption'+format)
    df = project.getAllInverterData()
    df.index.name = 'Timestamp'
    df.to_csv(fileName, sep=';')
    if (format == '.xlsx'):
        writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Consumption')
    else:
         df.to_csv(fileName, sep=';')


def exportCond(project):
    outputDir = str(outputDirectoryCond.value)
    format = str(formatSelectionCond.value)
    fileName=str(outputDir+'/'+str(project.name)+' condition'+format)
    GHIdf=project.GHIdf
    GHIdf=GHIdf.groupby(pd.TimeGrouper(freq='M')).mean().round(2)
    GHIdf.index = GHIdf.index.strftime('%m-%Y')
    if (format == '.xlsx'):
        writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
        GHIdf.to_excel(writer, sheet_name='Consumption')
    else:
         GHIdf.to_csv(fileName, sep=';')

def updateGeneralData(project):
        project.name=projectNameTxt.value
        project.contactPerson=projectContactTxt.value
        project.street=projectStreetTxt.value
        project.city=projectCityTxt.value
        project.telephoneNumber=projectTelephoneTxt.value
        project.projectOrientation=projectOrientation.value
        project.projectInclination=projectInclination.value
        project.projectLatitude=projectLatitude.value
        project.projectLongitude=projectLongitude.value
        project.structureType=structureDD.value
        project.totalkWP =float(total.value.replace(',','.'))
        project.totalkw = float(totalkw.value.replace(',','.'))
        project.totExtra = totExtra.value
        DH.saveProject(project)
        time.sleep(1)
        showManagementScreen('ID'+str(project.DBID))



def updateInverterData(project,inverter,inverter1Type,inverter1Tot,inverter1Totkw,inverter1Extra,inverter1SampleRate,filePick1,fileColumn1):
    inverter.type=inverter1Type.value
    inverter.kWP=float(inverter1Tot.value.replace(',','.'))
    inverter.kW=float(inverter1Totkw.value.replace(',','.'))
    inverter.extra =inverter1Extra.value
    inverter.filePath=filePick1.value
    if (fileColumn1.value!=""):
        inverter.columnNumber=int(fileColumn1.value)
    else:
        inverter.columnNumber=1
    inverter.sampleRate= inverter1SampleRate.value
    DH.saveProject(project)
    time.sleep(1)
    showManagementScreen('ID'+str(project.DBID))


def deleteInverter(project,inveterID,inverter):
    project.removeInverter(inveterID,inverter)
    DH.saveProject(project)
    time.sleep(1)
    showManagementScreen('ID'+str(project.DBID))

def cancelNewInverter(project):
       showManagementScreen('ID'+str(project.DBID))

def saveNewInverter(project,inverterXType,inverterXTotKWP,inverterXTotKW,inverterXExtra,inverterXSampleRate,filePickX,fileColumnX):
    type=inverterXType.value
    kWP=float(inverterXTotKWP.value.replace(',','.'))
    kW=float(inverterXTotKW.value.replace(',','.'))
    extra =inverterXExtra.value
    filePath=filePickX.value
    if (fileColumnX.value!=""):
        columnNumber=int(fileColumnX.value)
    else:
        columnNumber=1
    sampleRate= inverterXSampleRate.value
    inverter = Inverter(type,kWP,kW,extra,filePath,columnNumber,[],sampleRate)
    project.addInverter(inverter)
    DH.saveProject(project)
    time.sleep(1)
    showManagementScreen('ID'+str(project.DBID))



def addInverterLayout(inverterID,project):
    inverterID=int(inverterID)+1
    oldLayout=newLayout
    inverterXType = TextInput(value="20000TL-30", title="Inverter "+str(inverterID)+" type:")


    inverterXTotKWP = TextInput(value="20,5", title="Inverter "+str(inverterID)+" installed cap [kWP]:")
    inverterXTotKW = TextInput(value="20", title="Inverter "+str(inverterID)+" installed cap [kW]:")
    inverterXExtra = TextInput(value="", title="Inverter "+str(inverterID)+" EXTRA:")
    inverterXSampleRate = TextInput(value="15Min", title="Sample rate (e.g.'15Min','1H'):")


    filePickX = TextInput(value="/Users/christiaan/Desktop/Solcor/dataMergeWeek/Neuces2/Nueces/Nueces", title="Inverter "+str(inverterID)+" data:")
    fileColumnX = TextInput(value="1", title="Inverter "+str(inverterID)+" column nr in file:")

    buttonSave = Button(label='Save new Inverter')
    buttonSave.on_click(partial(saveNewInverter,project,inverterXType,inverterXTotKWP,inverterXTotKW,inverterXExtra,inverterXSampleRate,filePickX,fileColumnX))

    buttonCancel = Button(label='Cancel')
    buttonCancel.on_click(partial(cancelNewInverter,project))

    inverterXRow1= [inverterXType,inverterXTotKWP,inverterXTotKW]
    inverterXRow2= [inverterXExtra,filePickX,fileColumnX,inverterXSampleRate,buttonSave,buttonCancel]


    divX = [Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)]

    oldLayout.insert(15+3*int(inverterID),inverterXRow1)
    oldLayout.insert(16+3*int(inverterID),inverterXRow2)
    oldLayout.insert(17+3*int(inverterID),divX)

    del oldLayout[17+3*int(inverterID)+1]

    updatedLayout = oldLayout[:]
    globNewLayout.children = []
    globNewLayout.children=[layout(updatedLayout)]

def changeSolargisLocation(project,solargisLocation,year):
    year = year.value
    project.updateSolargisFile(solargisLocation.value,str(year))
    DH.saveProject(project)
    time.sleep(1)
    showManagementScreen('ID'+str(project.DBID))

def deleteProjectAndGoBack(project):
    DH.deleteProject(project)
    goToHomescreen()


def deleteProjectScreen(project):
    headingTxt = Div(text="""<p style="font-size:28px;text-align: center"> Delete: """+str(project.name),
            width=400, height=30)

    headingdiv = Div(text="""<hr noshade size=4 color=green>""",
        width=400, height=10)

    buttonDeleteProject=Button(label='Delete project',button_type="danger")
    buttonDeleteProject.on_click(partial(deleteProjectAndGoBack,project))
    buttonCancelDeletion=Button(label='Cancel')
    buttonCancelDeletion.on_click(partial(showManagementScreen,'ID'+str(project.DBID)))

    newLayout=[[headingTxt],[headingdiv],[buttonDeleteProject],[buttonCancelDeletion]]
    globNewLayout.children = []
    globNewLayout.children=[layout(newLayout)]


def showManagementScreen(ID):
    project = DH.getProject(int(ID[2:]))

    headingTxt = Div(text="""<p style="font-size:28px;text-align: center"> """+str(project.name),
            width=1100, height=30)


    generalTitle = Div(text="""<p style="font-size:24px;text-align: left"> General information""",
            width=1000, height=10)

    headingdiv = Div(text="""<hr noshade size=4 color=green>""",
        width=1100, height=10)



    global globNewLayout,newLayout,cleaningDateX,gridProbDateX,maintenanceDateX,internetProblemDateX,extraCommentX,\
        extraCommentDateX,formatSelection,formatSelectionCond,outputDirectory,outputDirectoryCond

    global projectNameTxt,projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt,projectOrientation,\
        projectInclination,projectLatitude,projectLongitude,structureDD,total,totalkw,totExtra


    projectNameTxt = TextInput(value=project.name, title="Project name:")


    projectContactTxt = TextInput(value=project.contactPerson, title="Contact person:")
    projectStreetTxt = TextInput(value=project.street, title="Street + nr:")
    projectCityTxt = TextInput(value=project.city, title="City (+ Country):")
    projectTelephoneTxt = TextInput(value=project.telephoneNumber, title="Telephone:")

    div0 = Div(text="""<hr noshade size=4 color=green>""",
        width=1100, height=30)

    projectOrientation =TextInput(value=str(project.projectOrientation), title="Project orientation:")
    projectInclination = TextInput(value=str(project.projectInclination), title="Project inclination:")
    projectLatitude = TextInput(value=str(project.projectLatitude), title="Project latitude:")
    projectLongitude = TextInput(value=str(project.projectLongitude), title="Project longitude:")


    structureDD = Select(title='Structure', value=str(project.structureType), options=["Parallel to roof","Structure with inclination"])


    div = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)


    total = TextInput(value=str(project.totalkWP), title="Total installed cap [kWP]:")
    totalkw = TextInput(value=str(project.totalkw), title="Total installed cap [kW]:")
    totExtra = TextInput(value=str(project.totExtra), title="Total Extra:")


    div2 = Div(text="""<hr noshade size=4 color=green>""",
        width=1100, height=30)


    buttonUpdateGeneralData = Button(label="Save changes")
    buttonUpdateGeneralData.on_click(partial(updateGeneralData,project))

    inverterLabels=[]
    lastInverterID=0
    for inveterTuple in project.inverters:
        inverterID = str(inveterTuple[0]+1)
        lastInverterID = inverterID
        inverter = inveterTuple[1]

        inverter1Type = TextInput(value=inverter.type, title="Inverter "+inverterID+" type:")
        inverter1Tot = TextInput(value=str(inverter.kWP), title="Inverter "+inverterID+" installed cap [kWP]:")
        inverter1Totkw = TextInput(value=str(inverter.kW), title="Inverter "+inverterID+" installed cap [kW]:")
        inverter1Extra = TextInput(value=str(inverter.extra), title="Inverter "+inverterID+" EXTRA:")
        inverter1SampleRate = TextInput(value=str(inverter.sampleRate), title="Sample rate (e.g.'15Min','1H'):")

        filePick1 = TextInput(value=str(inverter.filePath), title="Inverter "+inverterID+" data:")
        fileColumn1 = TextInput(value=str(inverter.columnNumber), title="Inverter "+inverterID+" column nr in file:")

        upDateInveterButton=Button(label='Save changes')
        upDateInveterButton.on_click(partial(updateInverterData,project,inverter,inverter1Type,inverter1Tot,inverter1Totkw,inverter1Extra,inverter1SampleRate,filePick1,fileColumn1))

        deleteInverterButton=Button(label='Delete')
        deleteInverterButton.on_click(partial(deleteInverter,project,int(inverterID)-1,inverter))

        div4 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)
        inverterLabels.append([inverter1Type,inverter1Tot,inverter1Totkw,inverter1Extra,filePick1,fileColumn1,inverter1SampleRate,upDateInveterButton,deleteInverterButton,div4])


    buttonAddInveter = Button(label='Add inverter')
    buttonAddInveter.on_click(partial(addInverterLayout,lastInverterID,project))


    div3 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)
    div4 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=10)


    MaintenanceTitle = Div(text="""<p style="font-size:24px;text-align: left"> Maintenance""",
            width=1000, height=10)

    cleaningDateX = TextInput(value="", title="Cleaning date(s):")
    gridProbDateX = TextInput(value="", title="Grid problem date(s):")
    maintenanceDateX = TextInput(value="", title="Maintenance date(s):")
    internetProblemDateX = TextInput(value="", title="Internet problem date(s):")


    extraComments = TextInput(value=str(project.commentList), title="Comments:")


    buttonBack = Button(label="Back")
    buttonBack.on_click(goToHomescreen)

    statusBanner=Div(text="""<p style="font-size:14px ;text-align: center">""",
    width=1100, height=100)

    div7 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)
    div8 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=10)
    inverterTitle = Div(text="""<p style="font-size:24px;text-align: left"> Inverter(s)""",
            width=1000, height=10)

    newLayout = [[headingTxt],[],[],[],[generalTitle],[headingdiv],[projectNameTxt],[projectContactTxt,projectStreetTxt,projectCityTxt,projectTelephoneTxt],[div0],[projectLatitude,projectLongitude,structureDD],[projectOrientation,projectInclination],
                 [div],[total,totalkw,totExtra],[div2],[buttonUpdateGeneralData],[],[],[],[inverterTitle],[div8]]



    for inverterInfo in inverterLabels:
        newLayout.append(inverterInfo)

    data = dict(
        dates=[],
        maintenance=[],
    )
    for cleanindate in project.cleaningDates:
        data['dates'].append(cleanindate)
        data['maintenance'].append('cleaning')
    for gridProb in project.gridProblemData:
        data['dates'].append(gridProb)
        data['maintenance'].append('Grid problems')
    for maint in project.maintenanceData:
        data['dates'].append(maint)
        data['maintenance'].append('Maintenance')
    for intProb in project.internetProblems:
        data['dates'].append(intProb)
        data['maintenance'].append('Internet problems')
    source = ColumnDataSource(data)

    columns = [
        TableColumn(field="dates", title="Date", formatter=DateFormatter(format='d M yy')),
        TableColumn(field="maintenance", title="Maintenance"),
    ]
    data_table = DataTable(source=source, columns=columns, width=400, height=200)
    source.on_change('selected', saveSelection)

    buttonMaintenanceMgmt = Button(label="Remove instance")
    buttonMaintenanceMgmt.on_click(partial(removeMaintenance, project,data_table))
    butttonAddMaintanceDate = Button(label="Add instance")
    butttonAddMaintanceDate.on_click(partial(collectNewMaintanceData,project))
    div5 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)

    for info in [[buttonAddInveter],[],[],[],[MaintenanceTitle],[div4],[data_table,cleaningDateX,gridProbDateX,maintenanceDateX,internetProblemDateX,buttonMaintenanceMgmt,butttonAddMaintanceDate],[div5]]:
        newLayout.append(info)


    dataNew = dict(
        dates=[],
        comment=[],
    )
    for comment in project.commentList:
        dataNew['dates'].append(datetime.datetime.strptime(str(comment[0]), '%d-%m-%Y'))
        dataNew['comment'].append(comment[1])
    source2 = ColumnDataSource(dataNew)

    columns = [
        TableColumn(field="dates", title="Date", formatter=DateFormatter(format='d M yy'),width=200),
        TableColumn(field="comment", title="Comments",width=1000),
    ]
    data_table2 = DataTable(source=source2, columns=columns, width= 1000, height=200)
    source2.on_change('selected', commentSelection)

    extraCommentX = TextInput(value="", title="Comment:")
    extraCommentDateX = TextInput(value="10-04-2017", title="Date comment:")
    removeCommentButton = Button(label="Remove Comment")
    removeCommentButton.on_click(partial(removeComment,project,data_table2))
    addCommentButton = Button(label="Add Comment")
    addCommentButton.on_click(partial(addComment,project))

    commentTitle = Div(text="""<p style="font-size:24px;text-align: left"> Comments""",
            width=1000, height=10)
    div9 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)


    dataTitle = Div(text="""<p style="font-size:24px;text-align: left"> Production data""",
            width=1000, height=10)
    div10 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)

    for info in [[],[],[],[commentTitle],[div9],[data_table2],[extraCommentDateX,extraCommentX,removeCommentButton,addCommentButton],[div3],[],[],[],[dataTitle],[div10]]:
        newLayout.append(info)


    ###production data information:
    df = project.getAllInverterData().round(2)
    df['Date'] = pd.to_datetime(df.index).strftime('%d/%m/%Y %H:%M:%S')
    DFdata = dict(df)
    DFsource = ColumnDataSource(DFdata)
    DFcolumns=[]
    headers= list(df)
    popped = headers.pop()
    headers.insert(0,popped)
    for columnName in headers:
        DFcolumns.append(TableColumn(field=columnName, title=columnName),)

    DFdata_table = DataTable(source=DFsource, columns=DFcolumns, width=500, height=600)

    outputDirectory=TextInput(value='',title='Output directory:')
    formatSelection = Select(title="Format:", value=".csv", options=[".csv", ".xlsx",])

    buttonExportCSV = Button(label="Export")
    buttonExportCSV.on_click(partial(export,project))

    ###Condition data

    solargisLocation = TextInput(value=project.solargisFileLocation, title="Solargis file location:")
    year = str(project.GHIdf.index.values[0])[0:4]

    solargisFileYear= TextInput(value=year, title="Solargis file year:")
    buttonChangeSolargis = Button(label="Update file")
    buttonChangeSolargis.on_click(partial(changeSolargisLocation,project,solargisLocation,solargisFileYear))

    dataConTitle = Div(text="""<p style="font-size:24px;text-align: left"> Condition data""",
            width=1000, height=10)
    div11 = Div(text="""<hr noshade size=4 color=green>""",width=1100, height=30)

    GHIdf = project.GHIdf
    GHIdf=GHIdf.groupby(pd.TimeGrouper(freq='M'))
    GHIdf=GHIdf.mean().round(2)
    GHIdf['Date'] = pd.to_datetime(GHIdf.index).strftime('%b %Y')
    GHIDFdata = dict(GHIdf)
    GHIDFsource = ColumnDataSource(GHIDFdata)
    GHIDFcolumns=[]
    GHIheaders= list(GHIdf)
    popped = GHIheaders.pop()
    GHIheaders.insert(0,popped)
    for columnName in GHIheaders:
        GHIDFcolumns.append(TableColumn(field=columnName, title=columnName),)

    GHIDFdata_table = DataTable(source=GHIDFsource, columns=GHIDFcolumns, width=400, height=320)

    outputDirectoryCond=TextInput(value='',title='Output directory:')
    formatSelectionCond = Select(title="Format:", value=".csv", options=[".csv", ".xlsx",])

    buttonExportCSVCond = Button(label="Export")
    buttonExportCSVCond.on_click(partial(exportCond,project))

    separationdiv = Div(text="""""",
        width=400, height=20)

    deleteProjectButton = Button(label="Delete project",button_type="danger")
    deleteProjectButton.on_click(partial(deleteProjectScreen,project))


    for info in [[DFdata_table],[outputDirectory],[formatSelection],[buttonExportCSV],[],[],[],[dataConTitle],[div11],[solargisLocation,solargisFileYear],[buttonChangeSolargis],[GHIDFdata_table],[outputDirectoryCond],[formatSelectionCond],[buttonExportCSVCond],[div7],[],[],[],[buttonBack,separationdiv,deleteProjectButton]]:
        newLayout.append(info)
    globNewLayout.children = []
    globNewLayout.children=[layout(newLayout)]




def showPreInspection(ID):
    project = DH.getProject(int(ID[2:]))
    global globNewLayout

    headingTxt = Div(text="""<p style="font-size:20px;text-align: center"> """+str(project.name),
            width=1000, height=30)

    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=20)

    title1Txt = Div(text="""<p style="font-size:16px;text-align: left"><u> Inspection period:</u>""",
            width=180, height=10)
    projectDateBegin = TextInput(value="01-04-2017 00:00:00", title="Begin date:")
    projectDateEnd = TextInput(value="30-04-2017 23:45:00", title="End date:")

    inspectButton = Button(label="Inspect")
    inspectButton.on_click(partial(collectInspectionData,project,projectDateBegin,projectDateEnd))

    sepdiv = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=20)

    buttonBack = Button(label="Back")
    buttonBack.on_click(goToHomescreen)



    lay = layout([[headingTxt],[div],[title1Txt],[projectDateBegin,projectDateEnd,inspectButton],[sepdiv],[buttonBack]])

    globNewLayout.children = []
    globNewLayout.children =[lay]




def manageProject(attr, old, new):
    showManagementScreen(new)

def inspectProject(attr, old, new):
    showPreInspection(new)


def saveSettings(middleLayout):
    settings=[]
    for setting in middleLayout:
        settings.append((setting.title,setting.value))
    print('New settings: '+str(settings))
    DH.setSettings(settings)
    goToHomescreen()

def resetSettings():
    DH.resetSettings()
    showSettingsScreen()

def ResetDBAndReturnToHome():
    DH.resetDB()
    goToHomescreen()

def reloadDBAndReturnToHome():
    DH.reloadDB()
    goToHomescreen()

def confirmDeleteDB():
    headingTxt = Div(text="""<p style="font-size:28px;text-align: center"> Reset Database: """,
            width=400, height=30)

    headingdiv = Div(text="""<hr noshade size=4 color=green>""",
        width=400, height=10)

    buttonDeleteProject=Button(label='Reset database',button_type="danger")
    buttonDeleteProject.on_click(partial(ResetDBAndReturnToHome))
    buttonCancelDeletion=Button(label='Cancel')
    buttonCancelDeletion.on_click(showSettingsScreen)

    newLayout=[[headingTxt],[headingdiv],[buttonDeleteProject],[buttonCancelDeletion]]
    globNewLayout.children = []
    globNewLayout.children=[layout(newLayout)]

def showSettingsScreen():
    headingTxt = Div(text="""<p style="font-size:20px;text-align: center"> Settings """,
            width=1000, height=30)
    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    settingsDict=DH.getSettings()
    middleLayout=[]

    k = list(settingsDict.keys())
    k.sort()
    for settingLabel in k:
        middleLayout.append(TextInput(value=str(settingsDict[settingLabel]), title=settingLabel))


    saveSettingsButton=Button(label='Save settings')
    saveSettingsButton.on_click(partial(saveSettings,middleLayout))

    buttonBack = Button(label="Back")
    buttonBack.on_click(goToHomescreen)

    resetButton = Button(label="Reset settings")
    resetButton.on_click(resetSettings)

    resetDBButton = Button(label="Reset Database",button_type="danger")
    resetDBButton.on_click(confirmDeleteDB)

    reloadDBButton = Button(label="Reload Database",)
    reloadDBButton.on_click(reloadDBAndReturnToHome)

    lay = layout([[headingTxt],[div],middleLayout,[saveSettingsButton],[resetButton],[resetDBButton],[reloadDBButton],[buttonBack]])

    globNewLayout.children = []
    globNewLayout.children =[lay]


def homescreen(firstTime):
    if firstTime:
        PE.updateAllProjects()
        print('projects updated')
        print('list',[(project.name,project.DBID,len(project.inverters[0][1].inverterData)) for project in DH.getAllSavedProjects()])

    global globNewLayout

    welcomeTxt = Div(text="""<p style="font-size:20px;text-align: center"> Solcor operational dashboard """,
            width=1000, height=30)

    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    buttonOngoingProjects = Button(label="Project dashboard",)
    #buttonOngoingProjects.on_click(partial(showProjectMenu, TotalData,means,magnification,kWhPerDay,totalkWh,rain))

    buttonAddNewProject = Button(label="Add new project")
    buttonAddNewProject.on_click(partial(createNewProjectScreen,))


    menu = [(str(project.name),"ID"+str(project.DBID)) for project in DH.getAllSavedProjects()]

    manageDropDown = Dropdown(label="Manage projects", button_type="warning", menu=menu)
    manageDropDown.on_change('value',partial(manageProject))


    inspectdropdown = Dropdown(label="Inspect Projects", button_type="warning", menu=menu)
    inspectdropdown.on_change('value', partial(inspectProject))


    buttonShowDashboard = Button(label="Dashboard")

    buttonCreateQuickReport = Button(label="Create quick report")
    buttonCreateQuickReport.on_click(partial(createNewProjectScreen,quickReport=True))

    buttonSettings = Button(label="Settings")
    buttonSettings.on_click(showSettingsScreen)



    #inspectdropdown.on_click(function_to_call)


    #url = path2url('Users/christiaan/PycharmProjects/dataMerger/static/SolcorBanner2.png')
    #print(url)

    divPicture = Div(text="<img src=https://dl.dropboxusercontent.com/s/kv1p5r6hvjpwi4z/Solcor%20logo.jpg?dl=0>")

    lay = layout([[divPicture],[welcomeTxt],[div],[buttonAddNewProject,manageDropDown,buttonSettings],[buttonShowDashboard,inspectdropdown,buttonCreateQuickReport]])


    globNewLayout.children = []
    globNewLayout.children =[lay]

def goToMainScreen():
    mainscreen(False)

def saveModus():
    headingTxt = Div(text="""<p style="font-size:20px;text-align: center"> Save modus """,
            width=1000, height=30)
    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    buttonBack = Button(label="Back")
    buttonBack.on_click(goToMainScreen)

    resetButton = Button(label="Reset settings")
    resetButton.on_click(resetSettings)

    resetDBButton = Button(label="Reset Database",button_type="danger")
    resetDBButton.on_click(confirmDeleteDB)

    reloadDBButton = Button(label="Reload Database",)
    reloadDBButton.on_click(reloadDBAndReturnToHome)

    lay = layout([[headingTxt],[div],[resetButton],[resetDBButton],[reloadDBButton],[buttonBack]])

    globNewLayout.children = []
    globNewLayout.children =[lay]



def mainscreen(firstTime):
    global globNewLayout
    global cloudyDaythresholdPercentage
    global rainyDaythresholdPercentage
    cloudyDaythresholdPercentage = float(DH.getSettings()['Cloudy day percentage'])
    rainyDaythresholdPercentage = float(DH.getSettings()['Rainy day percentage'])



    divPicture = Div(text="<img src=https://dl.dropboxusercontent.com/s/kv1p5r6hvjpwi4z/Solcor%20logo.jpg?dl=0>")

    welcomeTxt = Div(text="""<p style="font-size:20px;text-align: center"> Solcor operational dashboard """,
            width=1000, height=30)

    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)

    buttonEnter = Button(label="Go to dashboard")
    buttonEnter.on_click(partial(homescreen,True))

    buttonSettings = Button(label="Save modus")
    buttonSettings.on_click(saveModus)

    lay = layout([[divPicture],[welcomeTxt],[div],[buttonEnter,buttonSettings]])
    if firstTime:
        globNewLayout=lay
        curdoc().add_root(globNewLayout)
    else:
        globNewLayout.children = []
        globNewLayout.children =[lay]



mainscreen(True)

curdoc().title = "Solcor operations"






