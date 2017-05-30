__author__ = 'christiaanleysen'


import solcorEngine
import datetime



from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib.units import mm


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


def makePDFReport(project,beginDate,endDate,reportNumber,outputDir):

    todayString = datetime.date.today().strftime("%B %d, %Y")
    doc = SimpleDocTemplate(outputDir+'/Solcor injection analysis report '+unicode(str(project.name).decode('utf-8')) +beginDate' '+todayString+'.pdf', pagesize = A4, title = 'Solcor injection rate Report ', author ='christiaan' )

    print('Creating PDF...')


    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']
    styleHeading = styles['Heading1']
    styleHeading.alignment = 1 # centre text (TA_CENTRE)


    story = []



    # Text is added using the Paragraph class
    story.append(Spacer(inch, -1*inch))
    story.append(Image('SolcorBanner.png',20*cm, 4*cm))
    story.append(Paragraph(project.contactPerson, styleNormal))
    story.append(Paragraph(project.name, styleNormal))
    story.append(Paragraph(project.street, styleNormal))
    story.append(Paragraph(project.city, styleNormal))
    story.append(Paragraph(project.telephoneNumber, styleNormal))
    story.append(Paragraph('Report: '+reportNumber))




    story.append(Spacer(inch, .05*inch))

    story.append(Paragraph('<font color=rgb(73,75,88) size="20"><u> PV performance report</u></font>', styleHeading))
    story.append(Spacer(inch, .2*inch))
    story.append(Paragraph('<font color=rgb(73,75,88)><u>Site information</u></font>', styleHeading))

    story.append(Paragraph('longitude/latitude: '+project.projectLongitude+'° / '+project.projectLatitude+'°', styleNormal))
    story.append(Paragraph('Orientation/Inclination: '+project.projectOrientation+'° / '+project.projectInclination+'°', styleNormal))
    story.append(Paragraph('Orientation/Inclination: '+project.projectOrientation+'° / '+project.projectInclination+'°', styleNormal))




    story.append(Paragraph('PV installation: '+ str('{0:,}'.format(int(panelKWp)).replace(',', ' '))+' kWp', styleNormal))
    story.append(Paragraph('Total production: '+ str('{0:,}'.format(int(totalProduction)).replace(',', ' '))+' kWh', styleNormal))
    story.append(Paragraph('Total consumption: '+ str('{0:,}'.format(int(totalConsumption)).replace(',', ' '))+' kWh', styleNormal))



    story.append(Paragraph('<font color=rgb(73,75,88)><u>Yearly</u></font>', styleHeading))
    story.append(Paragraph('<font color=rgb(73,75,88) size="10"> Expected injection rate: '+ str(injectionR*100) +' %</font>', styleHeading))
    story.append(Spacer(inch, -.1*inch))
    # Images just need a filename and dimensions it should be printed at
    story.append(Image('plot.png',20*cm, 4.5*cm))
    # Spacers and pagebreaks help with presentation e.g.
    #story.append(PageBreak())
    # Data can be best presented in a table. A list of lists needs to declared first
    if (details != []):
        story.append(Paragraph('<font color=rgb(73,75,88)><u>Detailed periods</u></font>', styleHeading))
        i=0
        for x in details:
            story.append(Paragraph('<font color=rgb(73,75,88) size="10"> Expected injection rate: '+ str(x[0]*100) +' %</font>', styleHeading))
            story.append(Spacer(inch, -.1*inch))
            story.append(Image('plot'+str(i)+'.png',20*cm, 4.5*cm))
            i+=1
    if (comment != ''):
        story.append(Paragraph('<font color=rgb(73,75,88)><u>Comments</u></font>', styleHeading))
        story.append(Paragraph(comment, styleNormal))





    doc.build(story, onFirstPage=addPageNumber, onLaterPages=addPageNumber)

    print("PDF created!")

'''
beginDateCon = '2015-06-01 00:15:00' #'2015-06-01 00:15:00'
endDateCon = '2016-06-01 03:00:00' #'2016-05-22 03:00:00'

beginDateProd = '2015-06-01 00:15:00'
endDateProd = '2016-06-01 03:00:00'

comment='This is a comment that can be added to the report to clarify things.'

#makePDFReport(beginDateProd,endDateProd,beginDateCon,endDateCon,'15Min',[['2015-08-01 00:15:00','2015-08-31 23:45:00'],['2015-08-01 00:15:00','2015-08-31 23:45:00'],['2015-08-01 00:15:00','2015-08-31 23:45:00']],comment,detailed=True)
'''