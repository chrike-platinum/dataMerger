# -*- coding: utf-8 -*-
__author__ = 'christiaanleysen'



import datetime
import pandas as pd
import re
import dataHandler as DH
import os



from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, Table, TableStyle,PageTemplate, Frame,NextPageTemplate
from reportlab.lib.units import cm
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors

def createReadableDate(date):
    date = pd.to_datetime(date)
    date = date.date()
    date = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%d-%m-%Y')
    return date

def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    text = str(page_num)
    canvas.drawRightString(200*mm, 20*mm, text)




def coord(doc, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, doc.height -  y * unit
        return x, y




def createParagraph(c,doc, ptext, x, y, style=None):
        """"""
        if not style:
            style = doc.styles["Normal"]
        p = Paragraph(ptext, style=style)
        p.wrapOn(c, doc.width, doc.height)
        p.drawOn(c, *coord(doc,x, y, mm))


def createInfoBlock(c,y,doc,leftTitle,leftList,rightTitle,rightList,styleNormal,styleHeading):

    frameLTitle = Frame(doc.leftMargin+30, doc.bottomMargin, doc.width/2-5, doc.height-y*mm, id='col1')
    frameRTitle = Frame(doc.leftMargin+30+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               doc.height-y*mm, id='col2')

    frameLTitle.addFromList([Paragraph('<font color=rgb(73,75,88) size="13"><u>'+leftTitle+'</u></font>', styleNormal)],c)
    frameRTitle.addFromList([Paragraph('<font color=rgb(73,75,88) size="13"><u>'+rightTitle+'</u></font>', styleNormal)],c)


    frameLList = Frame(doc.leftMargin-30, doc.bottomMargin, doc.width/2-6, doc.height-1.05*y*mm, id='col3')
    frameRList = Frame(doc.leftMargin-20+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               doc.height-1.05*y*mm, id='col4')

    leftInformation = []
    for tupleL in leftList:
        leftInformation.append(Paragraph(str(tupleL[0])+': '+str(tupleL[1])+'TODO',styleNormal))

    rightInformation = []
    for tupleR in rightList:
        rightInformation.append(Paragraph(str(tupleR[0])+': '+str(tupleR[1])+'TODO',styleNormal))

    frameLList.addFromList(leftInformation,c)
    frameRList.addFromList(rightInformation,c)

def makeTable(list,column1Width,column2Width):
    LIST_STYLE = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.Color(0.496,0.723,0.234)),
    ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
    ('LINEBELOW', (0,-1), (-1,-1), 2, colors.Color(0.496,0.723,0.234))])

    data=list
    table = Table(data, colWidths=[column1Width,column2Width],style=LIST_STYLE)

    #table.wrapOn(c, 100, 20)
    return table



def drawCommentBox(c,doc,x,y,width,height,text,styleSmallHeading):
    ptext='<font color=rgb(73,75,88) size=10>Comment:</font>'
    createParagraph(c,doc, ptext, x-27, y+187, styleSmallHeading)

    c.setStrokeColorRGB(0.496,0.723,0.234)
    LIST_STYLE = TableStyle([('BOX', (0,0), (-1,0), 1, colors.Color(0.496,0.723,0.234)),('VALIGN',(-1,-1),(-1,-1),'TOP')])
    text = re.sub("(.{99})", "\\1\n", text, 0, re.DOTALL)
    data=[[text]]
    table = Table(data, colWidths=[width],rowHeights=[height],style=LIST_STYLE)
    table.wrapOn(c, x, y)
    table.drawOn(c, x, y)


def createInfoBlockTable(c,y,doc,leftTitle,leftList,rightTitle,rightList,styleNormal,styleHeading,leftTitleOffset,rightTitleOffset,leftTableWidth,rightTablewidth):

    frameLTitle = Frame(doc.leftMargin+leftTitleOffset, doc.bottomMargin, doc.width/2-5, y*mm-230, id='col1')
    frameRTitle = Frame(doc.leftMargin+rightTitleOffset+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               y*mm-230, id='col2')

    frameLTitle.addFromList([Paragraph('<font color=rgb(73,75,88) size="13"><u>'+leftTitle+'</u></font>', styleNormal)],c)
    frameRTitle.addFromList([Paragraph('<font color=rgb(73,75,88) size="13"><u>'+rightTitle+'</u></font>', styleNormal)],c)


    frameLList = Frame(doc.leftMargin-20, doc.bottomMargin, doc.width/2-6, y*mm-249, id='col3')
    frameRList = Frame(doc.leftMargin+10+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               y*mm-249, id='col4')

    leftInformation = makeTable(leftList,leftTableWidth,rightTablewidth)
    rightInformation = makeTable(rightList,leftTableWidth,rightTablewidth)


    frameLList.addFromList([leftInformation],c)
    frameRList.addFromList([rightInformation],c)

#testMethod (not used)
def testPDF(tempPlotDir,isTechReportRequest=True):
    todayString = datetime.date.today().strftime("%B %d, %Y")
    doc = SimpleDocTemplate('test.pdf', pagesize = A4, title = 'Solcor injection rate Report ', author ='christiaan' )
    frameL = Frame(doc.leftMargin-30, doc.bottomMargin, doc.width/2-6, doc.height-5.3*cm, id='col1')
    frameR = Frame(doc.leftMargin-20+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               doc.height-5.3*cm, id='col2')
    #doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2])])
    frame =  Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normalFrame')

    print('Creating PDF...')

    c  = Canvas('mydoc.pdf')

    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']
    styleNormal.fontSize=10
    styleHeading = styles['Heading1']
    styleSmallHeading = styles['Heading2']
    styleHeading.alignment = 1 # centre text (TA_CENTRE)
    styleSmallHeading.aligment =1


    # Text is added using the Paragraph class
    #firstPage
    bannerFrame = Frame(0*cm, doc.height, 210*mm, 48*mm, id='normal')
    bannerFrame.addFromList([Image('SolcorBanner.png',20*cm, 4*cm)],c)
    print('banner added...')

    ptext='<font color=rgb(73,75,88) size="20"><u> PV performance report</u></font>'
    createParagraph(c,doc, ptext, 25, 0, styleHeading)

    ptext='<font color=rgb(73,75,88) size="14"> name todo</font>'
    createParagraph(c,doc, ptext, 25, 9, styleHeading)

    ptext='<font color=rgb(73,75,88) size="12"> 01/04/2017 - 30/04/2017 </font>'
    createParagraph(c,doc, ptext, 25, 15, styleHeading)

    ptext='<font color=rgb(73,75,88)>General information</font>'
    createParagraph(c,doc, ptext, 80, 24, styleSmallHeading)

    c.setStrokeColorRGB(0.496,0.723,0.234)
    c.line(10*mm,222*mm,200*mm,222*mm)



    story1=[]
    story1.append(Paragraph('Report: +reportNumber',styleNormal))
    story1.append(Paragraph('Date: +todayString',styleNormal))
    story1.append(Paragraph('project.contactPerson', styleNormal))
    story1.append(Paragraph('project.name', styleNormal))
    story1.append(Paragraph('project.street', styleNormal))
    story1.append(Paragraph('project.city', styleNormal))
    story1.append(Paragraph('project.telephoneNumber', styleNormal))
    frameL.addFromList(story1,c)
    print('client info added...')


    story2=[]
    story2.append(Paragraph('Installed capacity: + str(project.totalkWP)',styleNormal))
    story2.append(Paragraph('Nominal Installed capacity: + str(project.totalkw)',styleNormal))
    story2.append(Paragraph('Longitude/latitude: + str(project.structureType)',styleNormal))#longitude/latitude: '+str(project.projectLongitude)+'° / '+str(project.projectLatitude)+'°'
    story2.append(Paragraph('Orientation/Inclination: + 90 12 23 / 123 34 34',styleNormal)) #'Orientation/Inclination: '+str(project.projectOrientation)+'° / '+str(project.projectInclination)+'°'
    story2.append(Paragraph('Structure: + str(project.structureType)',styleNormal))
    frameR.addFromList(story2,c)


    ptext='<font color=rgb(73,75,88)>Global overview kW</font>'
    createParagraph(c,doc, ptext, 80, 72, styleSmallHeading)

    c.setStrokeColorRGB(0.496,0.723,0.234)
    c.line(10*mm,173*mm,200*mm,173*mm)

    #Add plot to pdf
    firstPlot = Image(tempPlotDir+'plot3.png',19.8*cm, 9*cm)
    firstPlot.drawOn(c, *coord(doc,5, 170, mm))

    frameL2 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height-15*cm, id='col1')
    frameR2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               doc.height, id='col2')

    leftList=[('Number of cloudy days',2),('Number of rainy days', 0)]
    rightList =[('Cleaning dates:',0),['Internet problems dates:',0],['Grid Problems dates:',0],['Maintenance dates:',0]]

    createInfoBlockTable(c,130,doc,"Weather information:",leftList,"Maintenance information:",rightList,styleNormal,styleHeading,30,30,3.9*cm, 4.7*cm)

    drawCommentBox(c,doc,1.5*cm,30,18*cm,2*cm,"Here is a long comment about some stuff and stuff.aakjhsjkhakjhdkjhaskjhdkhkjsahkjdhkjashjkdhkjashkjdhkjahsdkjhaskjhkjdhkjashkjdhasjkhkdjhkas  hdjhaskjhaksjhkjdhkjasjh jhdkjashkjhaskjhskjahkjd askjhkjsahjkdhskjhjkdsjkhsajhaskhljksd ",styleSmallHeading)


    #secondPage
    page_num = c.getPageNumber()
    c.drawString(15, 15, 'Solcor.org')
    c.drawString(570, 15, str(page_num))

    c.showPage()

    bannerFrame = Frame(0*cm, doc.height, 210*mm, 48*mm, id='normal')
    bannerFrame.addFromList([Image('SolcorBanner.png',20*cm, 4*cm)],c)

    ptext='<font color=rgb(73,75,88)>Global overview kWh & kWh/kWP</font>'
    createParagraph(c,doc, ptext, 65, 6, styleSmallHeading)

    c.setStrokeColorRGB(0.496,0.723,0.234)
    c.line(10*mm,240*mm,200*mm,240*mm)

    secondPlot = Image(tempPlotDir+'plot2.png',20*cm, 9*cm)
    secondPlot.drawOn(c, *coord(doc,5, 100, mm))

    leftList=[('Performance ratio:', '72.7'+'%'),('GHI daily:', '4.92'+' kWh/m^2'),('GII daily:', '5.72'+' kWh/m^2'),('Total production:', '5518'+' kWh'),('Real daily average:', '4.0'+' kWh/kWP')]
    rightList=[('Expected production:', '7588'+' kWh'),('Expected daily average:', '5.5'+' kWh/kWP'),('Expected daily average:', '252.93'+' kWh'),('Number of underperforming days:', '30'),('Number of overperforming days:', '0')]
    createInfoBlockTable(c,190,doc,'Real performance indicators:',leftList,'Estimated performance indicators:',rightList,styleNormal,styleHeading,10,10,6*cm,2.5*cm)


    page_num = c.getPageNumber()
    c.drawString(15, 15, 'Solcor.org')
    c.drawString(570, 15, str(page_num))
    c.showPage()

    if (isTechReportRequest):
    #thirdPage

        #do this for the first elements in list

        bannerFrame = Frame(0*cm, doc.height, 210*mm, 48*mm, id='normal')
        bannerFrame.addFromList([Image('SolcorBanner.png',20*cm, 4*cm)],c)

        ptext='<font color=rgb(73,75,88)>Inverter: overview kWh/kWP</font>'
        createParagraph(c,doc, ptext, 73, 6, styleSmallHeading)

        c.setStrokeColorRGB(0.496,0.723,0.234)
        c.line(10*mm,240*mm,200*mm,240*mm)

        secondPlot = Image(tempPlotDir+'plot1.png',20*cm, 9*cm)
        secondPlot.drawOn(c, *coord(doc,3, 100, mm))


        i=0
        for a in [0,0]:
            ptext='<font color=rgb(73,75,88) size="16"><u>Inverter 1%</U></font>'
            createParagraph(c,doc, ptext, 90, 110+i, styleSmallHeading)

            leftTitle='Inverter information:'
            leftList = [('Performance ratio:','70.0'+'%'),('Total production:', '2945'+' kWh'),('Expected production:', '4206'+' kWh'),('Real daily average:', '3.85'+' kWh/kWP')]
            rightList = [('Inverter type:', '25000TL-30'),('Installed capacity:', '25.5'+' kWP'),('Nominal installed capacity:', '25.0'+' kW'),('Expected daily average:', '5.5'+' kWh/kWP'),('Expected daily average:', '140.21'+' kWh')]
            rightTitle='Performance indicators:'


            createInfoBlockTable(c,135+i,doc,leftTitle,leftList,rightTitle,rightList,styleNormal,styleHeading,30,30,6*cm,3*cm)
            i+=57
        #if len(list)>2:
        page_num = c.getPageNumber()
        c.drawString(15, 15, 'Solcor.org')
        c.drawString(570, 15, str(page_num))
        c.showPage()
            #proceed on next page
        i=0
        counter = 1
        for a in [1,2,3,4,5,6]:

                if (counter!=0 and counter%4==0):
                    page_num = c.getPageNumber()
                    c.drawString(15, 15, 'Solcor.org')
                    c.drawString(570, 15, str(page_num))
                    c.showPage()
                    i=0

                bannerFrame = Frame(0*cm, doc.height, 210*mm, 48*mm, id='normal')
                bannerFrame.addFromList([Image('SolcorBanner.png',20*cm, 4*cm)],c)

                ptext='<font color=rgb(73,75,88)>Inverter: overview kWh/kWP</font>'
                createParagraph(c,doc, ptext, 73, 6, styleSmallHeading)

                c.setStrokeColorRGB(0.496,0.723,0.234)
                c.line(10*mm,240*mm,200*mm,240*mm)

                ptext='<font color=rgb(73,75,88) size="16"><u>Inverter 1%'+str(i)+'</U></font>'
                createParagraph(c,doc, ptext, 90, 20-i, styleSmallHeading)


                leftTitle='Inverter information:'
                leftList = [('Performance ratio:','70.0'+'%'),('Total production:', '2945'+' kWh'),('Expected production:', '4206'+' kWh'),('Real daily average:', '3.85'+' kWh/kWP')]
                rightList = [('Inverter type:', '25000TL-30'),('Installed capacity:', '25.5'+' kWP'),('Nominal installed capacity:', '25.0'+' kW'),('Expected daily average:', '5.5'+' kWh/kWP'),('Expected daily average:', '140.21'+' kWh')]
                rightTitle='Performance indicators:'

                createInfoBlockTable(c,280+i,doc,leftTitle,leftList,rightTitle,rightList,styleNormal,styleHeading,30,30,6*cm,3*cm)



                i-=57
                counter+=1

        page_num = c.getPageNumber()
        c.drawString(15, 15, 'Solcor.org')
        c.drawString(570, 15, str(page_num))

    c.save()



def makePDF(tempPlotDir,project,reportNr,beginDate,endDate,printObject,isTechReportRequest=True):
    outputLocation = DH.getSettings()['PDF-output directory']
    if outputLocation != '':
        outputLocation=outputLocation+'/'
    beginDate=createReadableDate(beginDate)
    endDate=createReadableDate(endDate)
    todayString = datetime.date.today().strftime("%d/%m/%Y")
    doc = SimpleDocTemplate(str(outputLocation)+'test.pdf', pagesize = A4, title = 'Solcor injection rate Report ', author ='ChristiaanLeysen' )
    frameL = Frame(doc.leftMargin-30, doc.bottomMargin, doc.width/2-6, doc.height-4.7*cm, id='col1')
    frameR = Frame(doc.leftMargin-20+doc.width/2+6, doc.bottomMargin, doc.width/2+30,
               doc.height-4.7*cm, id='col2')
    #doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2])])
    frame =  Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normalFrame')

    print('Creating PDF...')

    pdfName = 'Solcor PV performance analysis '+str(project.name)+' '+str(beginDate)+' '+str(endDate)+'.pdf'
    if isTechReportRequest:
        pdfName = 'Solcor PV performance analysis '+str(project.name)+' '+str(beginDate)+' '+str(endDate)+' (technical report)'+'.pdf'
    c = Canvas(os.path.join(str(outputLocation),pdfName))
    #c  = Canvas(str(outputLocation)+pdfName)

    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']
    styleNormal.fontSize=10
    styleHeading = styles['Heading1']
    styleSmallHeading = styles['Heading2']
    styleHeading.alignment = 1 # centre text (TA_CENTRE)
    styleSmallHeading.aligment =1


    # Text is added using the Paragraph class
    #firstPage
    bannerFrame = Frame(0*cm, doc.height, 210*mm, 48*mm, id='normal')
    bannerFrame.addFromList([Image('SolcorBanner.png',20*cm, 4*cm)],c)
    print('banner added...')

    ptext='<font color=rgb(73,75,88) size="20"><u> PV performance report</u></font>'
    createParagraph(c,doc, ptext, 25, 0, styleHeading)

    ptext='<font color=rgb(73,75,88) size="14"> '+project.name+'</font>'
    createParagraph(c,doc, ptext, 25, 9, styleHeading)

    ptext='<font color=rgb(73,75,88) size="12"> '+beginDate+' - '+endDate+' </font>'
    createParagraph(c,doc, ptext, 25, 15, styleHeading)

    ptext='<font color=rgb(73,75,88)>General information</font>'
    createParagraph(c,doc, ptext, 80, 22, styleSmallHeading)

    c.setStrokeColorRGB(0.496,0.723,0.234)
    c.line(10*mm,224*mm,200*mm,224*mm)



    story1=[]
    story1.append(Paragraph('Report: '+str(reportNr),styleNormal))
    story1.append(Paragraph('Date: '+todayString,styleNormal))
    story1.append(Paragraph(project.contactPerson, styleNormal))
    story1.append(Paragraph(project.name, styleNormal))
    story1.append(Paragraph(project.street, styleNormal))
    story1.append(Paragraph(project.city, styleNormal))
    story1.append(Paragraph(project.telephoneNumber, styleNormal))
    frameL.addFromList(story1,c)
    print('client info added...')


    story2=[]
    story2.append(Paragraph('Installed capacity: '+str(project.totalkWP),styleNormal))
    story2.append(Paragraph('Nominal Installed capacity: '+ str(project.totalkw),styleNormal))
    story2.append(Paragraph('longitude/latitude: '+str(project.projectLongitudeString)+" / "+str(project.projectLatitudeString),styleNormal))
    story2.append(Paragraph('Orientation/Inclination: '+str(project.projectOrientation)+'° / '+str(project.projectInclination)+'°',styleNormal))
    story2.append(Paragraph('Structure: '+ str(project.structureType),styleNormal))
    story2.append(Paragraph('Real-time data used: '+ str(printObject.realDataBoolean),styleNormal))
    for inveterTuple in project.inverters[0:5]:
        story2.append(Paragraph('inverter '+str(inveterTuple[0]+1)+': '+inveterTuple[1].type+' / '+str(inveterTuple[1].kWP)+' kWP' ,styleNormal))
    frameR.addFromList(story2,c)
    print('General info added...')


    ptext='<font color=rgb(73,75,88)>Global overview kW</font>'
    createParagraph(c,doc, ptext, 80, 75, styleSmallHeading)#72

    c.setStrokeColorRGB(0.496,0.723,0.234)
    c.line(10*mm,171*mm,200*mm,171*mm)

    #Add plot to pdf
    firstPlot = Image(tempPlotDir+'plot3.png',19.8*cm, 9*cm)
    firstPlot.drawOn(c, *coord(doc,5, 170, mm))

    frameL2 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height-15*cm, id='col1')
    frameR2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               doc.height, id='col2')

    leftList=[('Number of cloudy days:',str(printObject.nrOfCloudyDays)),('Number of rainy days:',str(printObject.nrOfRainyDays))]

    rightList =[('Cleaning dates:',str(printObject.cleaningDatestring)),('Internet problems dates:',str(printObject.internetProbString)),
                ('Grid Problems dates:',str(printObject.gridProbString)),('Maintenance dates:',str(printObject.maintenaceString))]

    createInfoBlockTable(c,130,doc,"Weather information:",leftList,"Maintenance information:",rightList,styleNormal,styleHeading,30,30,3.9*cm, 4.7*cm)


    commentString = ""
    for comment in printObject.extraCommentString:
        commentString+=str(comment)



    drawCommentBox(c,doc,1.5*cm,30,18*cm,2*cm,commentString,styleSmallHeading)
    print('First page ready...')


    #secondPage
    page_num = c.getPageNumber()
    c.drawString(15, 15, 'Solcor.org')
    c.drawString(570, 15, str(page_num))

    c.showPage()

    bannerFrame = Frame(0*cm, doc.height, 210*mm, 48*mm, id='normal')
    bannerFrame.addFromList([Image('SolcorBanner.png',20*cm, 4*cm)],c)

    ptext='<font color=rgb(73,75,88)>Global overview kWh & kWh/kWP</font>'
    createParagraph(c,doc, ptext, 65, 6, styleSmallHeading)

    c.setStrokeColorRGB(0.496,0.723,0.234)
    c.line(10*mm,240*mm,200*mm,240*mm)

    secondPlot = Image(tempPlotDir+'plot2.png',20*cm, 9*cm)
    secondPlot.drawOn(c, *coord(doc,5, 100, mm))


    leftList = [('Real performance ratio',str(printObject.totPR)+'%'),('GHI daily',str(printObject.GHIdaily)+' kWh/m^2'),('GII daily',str(printObject.GIIdaily)+' kWh/m^2'),('Real total production',str(round(printObject.totalGenerated,2))+' kWh'),
                     ('Real daily average',str(printObject.realDailyAvg)+' kWh/kWP'),('Real daily average',str(printObject.realDailyAvg*project.totalkWP)+' kWh')]

    rightlist = [('Expected performance ratio',str(printObject.expPR)+ '%'),('Expected daily average',str(printObject.expDailyAvg)+' kWh/kWP'),
                     ('Expected daily average',str(round((printObject.expDailyAvg*project.totalkWP),2))+' kWh'),('Expected monthly production',str(round((printObject.expDailyAvg*project.totalkWP*len(printObject.totalKWhPerday)),2))+' kWh'),
                 ('Number of underperforming days',printObject.underperfDays),('Number of overperforming days',printObject.overperfDays)]


    createInfoBlockTable(c,190,doc,'Real performance indicators:',leftList,'Estimated performance indicators:',rightlist,styleNormal,styleHeading,10,10,6*cm,2.5*cm)


    page_num = c.getPageNumber()
    c.drawString(15, 15, 'Solcor.org')
    c.drawString(570, 15, str(page_num))


    if (isTechReportRequest):
        print('adding technical information: '+str(isTechReportRequest))
        c.showPage()
    #thirdPage

        #do this for the first elements in list

        bannerFrame = Frame(0*cm, doc.height, 210*mm, 48*mm, id='normal')
        bannerFrame.addFromList([Image('SolcorBanner.png',20*cm, 4*cm)],c)

        ptext='<font color=rgb(73,75,88)>Inverter: overview kWh/kWP</font>'
        createParagraph(c,doc, ptext, 73, 6, styleSmallHeading)

        c.setStrokeColorRGB(0.496,0.723,0.234)
        c.line(10*mm,240*mm,200*mm,240*mm)

        secondPlot = Image(tempPlotDir+'plot1.png',20*cm, 9*cm)
        secondPlot.drawOn(c, *coord(doc,3, 100, mm))


        i=0
        inverterID=0


        for a in project.inverters[0:2]:
            inverter = a[1]
            ptext='<font color=rgb(73,75,88) size="16"><u>Inverter '+str(inverterID+1)+'</U></font>'
            createParagraph(c,doc, ptext, 90, 110+i, styleSmallHeading)

            rightTitle='Inverter information:'
            leftTitle='Performance indicators:'


            PR = printObject.invertersPR[inverterID]
            totalGenerated = printObject.invertersTotalGenerated[inverterID]
            realDailyAvg = printObject.invertersRealDailyAvgKWP[inverterID]
            expDailyAvg = printObject.invertersExpDailyAvgKWP[inverterID]


            leftList = [('Real performance ratio',PR+'%'),('Real total production',totalGenerated+' kWh'),
                     ('Real daily average',realDailyAvg+' kWh/kWP'),('Real daily average',str(float(realDailyAvg)*inverter.kWP)+' kWh')]

            rightList=[('Inverter type',str(inverter.type)),('Installed capacity',str(inverter.kWP)+' kWP'),('Nominal installed capacity',str(inverter.kW)+' kW'),
                   ('Expected daily average',expDailyAvg+' kWh/kWP'),('Expected daily average',str(round((float(expDailyAvg)*inverter.kW),2))+' kWh')]



            createInfoBlockTable(c,192-i,doc,leftTitle,leftList,rightTitle,rightList,styleNormal,styleHeading,30,30,6*cm,3*cm)
            i+=57
            inverterID+=1
        #if len(list)>2:
        page_num = c.getPageNumber()
        c.drawString(15, 15, 'Solcor.org')
        c.drawString(570, 15, str(page_num))

        if len(project.inverters[2:len(project.inverters)])!=0:
            c.showPage()
        i=0
        counter = 1
        for a in project.inverters[2:len(project.inverters)]:
                if (counter!=0 and counter%4==0):
                    page_num = c.getPageNumber()
                    c.drawString(15, 15, 'Solcor.org')
                    c.drawString(570, 15, str(page_num))
                    c.showPage()
                    i=0

                bannerFrame = Frame(0*cm, doc.height, 210*mm, 48*mm, id='normal')
                bannerFrame.addFromList([Image('SolcorBanner.png',20*cm, 4*cm)],c)

                ptext='<font color=rgb(73,75,88)>Inverter: overview kWh/kWP</font>'
                createParagraph(c,doc, ptext, 73, 6, styleSmallHeading)

                c.setStrokeColorRGB(0.496,0.723,0.234)
                c.line(10*mm,240*mm,200*mm,240*mm)

                ptext='<font color=rgb(73,75,88) size="16"><u>Inverter '+str(inverterID+1)+'</U></font>'
                createParagraph(c,doc, ptext, 90, 20-i, styleSmallHeading)


                rightTitle='Inverter information:'
                leftTitle='Performance indicators:'


                inverter = project.getInverter(inverterID)
                PR = printObject.invertersPR[inverterID]
                totalGenerated = printObject.invertersTotalGenerated[inverterID]
                realDailyAvg = printObject.invertersRealDailyAvgKWP[inverterID]
                expDailyAvg = printObject.invertersExpDailyAvgKWP[inverterID]


                leftList = [('Real performance ratio',PR+'%'),('Real total production',totalGenerated+' kWh'),
                     ('Real daily average',realDailyAvg+' kWh/kWP'),('Real daily average',str(float(realDailyAvg)*inverter.kWP)+' kWh')]

                rightList=[('Inverter type',str(inverter.type)),('Installed capacity',str(inverter.kWP)+' kWP'),('Nominal installed capacity',str(inverter.kW)+' kW'),
                   ('Expected daily average',expDailyAvg+' kWh/kWP'),('Expected daily average',str(round((float(expDailyAvg)*inverter.kW),2))+' kWh')]




                createInfoBlockTable(c,280+i,doc,leftTitle,leftList,rightTitle,rightList,styleNormal,styleHeading,30,30,6*cm,3*cm)



                i-=57
                counter+=1
                inverterID+=1

        page_num = c.getPageNumber()
        c.drawString(15, 15, 'Solcor.org')
        c.drawString(570, 15, str(page_num))
    print('saving PDF...')
    c.save()
    print('PDF: '+pdfName+' saved!')
    print('Location: '+str(os.path.join(str(outputLocation))))


