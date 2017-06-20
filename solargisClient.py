
import urllib2
import xml.etree.ElementTree as ET
from xml import etree
import pandas as pd
global APIkey
APIkey ='V4Vf064Jx4F1gbmsl8sl' #Replace if needed


def requestSolargisData(lat,lon,beginDate,EndDate,siteName,id,listOfRequests,samplerate,terrainShading):
    print('Collecting real GHI data from Solargis API...')
    namespaces = {'xmlns':"http://geomodel.eu/schema/ws/data",
                  'ns2':"http://geomodel.eu/schema/common/geo"}
    constructXMLrequest(lat,lon,beginDate,EndDate,siteName,id,listOfRequests,samplerate,terrainShading)
    request_xml = open('tempXML.xml').read()
    reponse_xml = doSolargisAPICall(request_xml)
    data=[]
    data = reponse_xml.findall('.//xmlns:row',namespaces)
    data = [tuple(reversed([a[1] for a in element.attrib.items()])) for element in data]
    print(data)
    data = [[el[0]]+el[1].split() for el in data]
    print(data)
    df = pd.DataFrame(data)
    columnames = ['timestamp'] + listOfRequests
    df.columns = columnames
    df['timestamp'] = df['timestamp'].astype(str).str[:-6]
    df.set_index('timestamp',inplace=True)
    return df




def constructXMLrequest(lat,lon,beginDate,EndDate,siteName,id,listOfRequests,samplerate,terrainShading):
    namespaces = {'CC':"http://geomodel.eu/schema/data/request",
    'ws':"http://geomodel.eu/schema/ws/data",
    'geo': "http://geomodel.eu/schema/common/geo",
    'pv': "http://geomodel.eu/schema/common/pv",
    'xsi' : "http://www.w3.org/2001/XMLSchema-instance"}


    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)
    tree = ET.parse('datadelivery_demo_request.xml')
    tree.getroot().set('dateFrom',beginDate)
    tree.getroot().set('dateTo',EndDate)
    tree.find('CC:site',namespaces).set('id',id)
    tree.find('CC:site',namespaces).set('name',siteName)
    tree.find('CC:site',namespaces).set('lat',lat)
    tree.find('CC:site',namespaces).set('lng',lon)
    tree.find('CC:processing',namespaces).set('key'," ".join(listOfRequests))
    tree.find('CC:processing',namespaces).set('summarization',samplerate)
    tree.find('CC:processing',namespaces).set('terrainShading',terrainShading)
    #tree.find('CC:timeZone',namespaces).set('GMT')

    tree.write('tempXML.xml')


def doSolargisAPICall(request_xml):
    api_key = APIkey
    url = 'https://solargis.info/ws/rest/datadelivery/request?key=%s' % api_key
    try:
          req = urllib2.Request(url)
          req.add_header('Content-Type', 'application/xml')
          response = urllib2.urlopen(req, request_xml)  # HTTP POST
          response_xml = response.read()
          response_xml = response_xml.replace('&#xD;', '')
          #print(response_xml)
          return ET.fromstring(response_xml)
    except urllib2.HTTPError as e:
          print 'Error message from the Solargis server: %s' % e.read()

