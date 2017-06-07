# -*- coding: utf-8 -*-
__author__ = 'christiaanleysen'



import datetime



from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, Table, TableStyle,PageTemplate, Frame,NextPageTemplate
from reportlab.lib.units import cm
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors


clientName = "Dummy name"
clientAddress="Dummy street 9"
clientLand="Chile"
clientTel="+32 000 00 00 00"


def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    text = str(page_num)
    canvas.drawRightString(200*mm, 20*mm, text)


def makePDFReport(project,projectDateBeginString,projectDateEndString,True,reportNumber,tempPlotDir,outputDir):

    todayString = datetime.date.today().strftime("%B %d, %Y")
    doc = SimpleDocTemplate('test.pdf', pagesize = A4, title = 'Solcor injection rate Report ', author ='christiaan' )
    frameL = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height-4*cm, id='col1')
    frameR = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               doc.height, id='col2')
    #doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2])])
    frame =  Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normalFrame')

    print('Creating PDF...')

    c  = Canvas('mydoc.pdf')

    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']
    styleHeading = styles['Heading1']
    styleHeading.alignment = 1 # centre text (TA_CENTRE)


    story = []




    # Text is added using the Paragraph class
    story.append(Spacer(inch, -1*inch))
    bannerFrame = Frame(0.5*cm, doc.topMargin, 20*cm, 4.1*cm, id='normal')
    bannerFrame.addFromList([Image('SolcorBanner.png',20*cm, 4*cm)],c)
    print('banner added...')

    story1=[]
    story1.append(Paragraph(project.contactPerson, styleNormal))
    story1.append(Paragraph(project.name, styleNormal))
    story1.append(Paragraph(project.street, styleNormal))
    story1.append(Paragraph(project.city, styleNormal))
    story1.append(Paragraph(project.telephoneNumber, styleNormal))
    story1.append(Paragraph('Report: '+reportNumber,styleNormal))
    frameL.addFromList(story1,c)
    print('client info added...')

    '''
    story.append(Spacer(inch, .05*inch))

    story.append(Paragraph('<font color=rgb(73,75,88) size="20"><u> PV performance report</u></font>', styleHeading))
    story.append(Spacer(inch, .2*inch))
    story.append(Paragraph('<font color=rgb(73,75,88)><u>Site information</u></font>', styleHeading))

    story.append(Paragraph('longitude/latitude: '+str(project.projectLongitude)+'° / '+str(project.projectLatitude)+'°', styleNormal))
    story.append(Paragraph('Orientation/Inclination: '+str(project.projectOrientation)+'° / '+str(project.projectInclination)+'°', styleNormal))
    story.append(Paragraph('Orientation/Inclination: '+str(project.projectOrientation)+'° / '+str(project.projectInclination)+'°', styleNormal))

    print(tempPlotDir+'plot3.png')
    story.append(Image(tempPlotDir+'plot3.png',20*cm, 4*cm))

    frame.addFromList(story,c)
    '''
    c.save()
    #story.append(NextPageTemplate('TwoCol'))
    #story.append(Paragraph("Frame two columns,  "*20,styles['Normal']))


    #doc.build(story, onFirstPage=addPageNumber, onLaterPages=addPageNumber)


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
        print('drawn')

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

    data= list
    table = Table(data, colWidths=[column1Width,column2Width],style=LIST_STYLE)

    #table.wrapOn(c, 100, 20)
    return table



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
    c.line(10*mm,174*mm,200*mm,174*mm)

    #Add plot to pdf
    firstPlot = Image(tempPlotDir+'plot3.png',20*cm, 9*cm)
    firstPlot.drawOn(c, *coord(doc,5, 170, mm))

    frameL2 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height-15*cm, id='col1')
    frameR2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               doc.height, id='col2')

    leftList=[('Number of cloudy days',2),('Number of rainy days', 0)]
    rightList =[('Cleaning dates:',0),['Internet problems dates:',0],['Grid Problems dates:',0],['Maintenance dates:',0],['Comment:','here is a coment']]

    createInfoBlockTable(c,130,doc,"Weather information:",leftList,"Maintenance information:",rightList,styleNormal,styleHeading,30,30,3.9*cm, 4.7*cm)

    #secondPage
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
        c.showPage()
            #proceed on next page
        i=0
        counter = 1
        for a in [1,2,3,4,5,6]:

                if (counter!=0 and counter%4==0):
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





    c.save()


testPDF('tempPlots/')