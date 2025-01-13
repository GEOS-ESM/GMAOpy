#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, May 2010, dev@synopticview.com
#-------------------------------------------------------------------
from twisted.internet import defer, reactor
from twisted.web import http

from semperpy.services.contents import Contents
from semperpy.services.errors import ServiceError

class Response(object):

    def __init__(self,request=None):
        self.request = request

    def setRequest(self,request):
        self.request = request

    def send_http_response(self,response,code):
        self.request.setHeader('Content-Type', 'application/json')
        self.request.write(Contents.encode(data=response, code = code))
        self.request.finish()

    def send(self,value,code):
        self.request.setResponseCode(http.OK)
        self.send_http_response(value,code)

    def __call__(self,service,execute,*args,**kargs):
        raise SystemError('Not implemented')
