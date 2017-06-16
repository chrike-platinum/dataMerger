
import urllib2
 
if __name__ == '__main__':
   request_xml = open('datadelivery_demo_request.xml').read()
   # alternatively, you obtain request_xml by marshalling from python object
   # print 'Request:', request_xml
   api_key = 'demo'
   url = 'https://solargis.info/ws/rest/datadelivery/request?key=%s' % api_key
   try:
      req = urllib2.Request(url)
      req.add_header('Content-Type', 'application/xml')
      response = urllib2.urlopen(req, request_xml)  # HTTP POST
      response_xml = response.read()
      response_xml = response_xml.replace('&#xD;', '')
      print 'Response:'
      print response_xml
   except urllib2.HTTPError as e:
      print 'Error message from the server: %s' % e.read()
   # parse response_xml and use data (alternatively, first unmarshall the response_xml back to python object)


