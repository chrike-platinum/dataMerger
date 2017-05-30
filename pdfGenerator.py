# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from xhtml2pdf import pisa
import codecs# import python module
import urllib
from os.path import abspath
from bs4 import BeautifulSoup
from GrabzIt import GrabzItClient

# Define your data
#f=codecs.open("test.html", 'r')
#with open(abspath('test4.html')) as fh:
    #sourceHtml =fh.read()

#soup = BeautifulSoup(sourceHtml)
#print(soup)



import cStringIO
import ho.pisa as pisa
import os


#os.system('wkhtmltopdf /hp2.html out2.pdf')

# Shortcut for dumping all logs on screen
#pisa.showLogging()

def HTML2PDF(data, filename, open=False):

    """
    Simple test showing how to create a PDF file from
    PML Source String. Also shows errors and tries to start
    the resulting PDF
    """

    pdf = pisa.CreatePDF(
        cStringIO.StringIO(data),
        file(filename, "wb"))

    if open and (not pdf.err):
        os.startfile(str(filename))

    return not pdf.err


outputFilename = "test.pdf"
'''
# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err

# Main program
if __name__=="__main__":
    pisa.showLogging()
    convertHtmlToPdf(sourceHtml, outputFilename)
'''

import pdfkit
pdfkit.from_file('banner.html', 'micro2.pdf')
pdfkit.from_url('file:///Users/christiaan/PycharmProjects/dataMerger/p2.html','m.pdf')
#pdfkit.from_string(sourceHtml,'microX.pdf')





'''
grabzIt = GrabzItClient.GrabzItClient("M2RlNGNmNTJkYTdjNDFkN2FkM2Y0N2M2ZjAyZTNhNjE=", "GQANH1A/FT86YD97MCoLPz9YUT9OYj8/Pz9zED82Pz8=")
grabzIt.HTMLToPDF(soup)
grabzIt.SaveTo("result.pdf")
'''