#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, May 2010, dev@synopticview.com
#-------------------------------------------------------------------
from twisted.web import server

from semperpy.services.contents import Contents
from semperpy.services.response import Response
from semperpy.services.errors import ServiceError, BadRequest
from semperpy.services.resource import Resource

class Service(Resource):

    isLeaf = True

    def __init__(self,name,services,pages,response):
        Resource.__init__(self)
        self.name = name
        self.services = services
        self.pages = pages
        self.response = response


    def find_handler(self,postpath,handlers):
        key = None
        if len(postpath) == 0 or postpath[0] == "":
            key = handlers
        elif postpath[0] in handlers:
            key = self.find_handler(postpath[1:],handlers[postpath[0]])    
        if not key:
            raise BadRequest("No handler for '%s' found" % postpath[0])
        return key

    def render_POST(self, request):
        self.response.setRequest(request)
        handler = None
        try:
            body = request.content.read()
            body = Contents.decode(body)
            handler = self.find_handler(request.postpath,self.services)['action']
        except ServiceError as e:
            self.response.send(e.__str__(),e.response_code())
            return server.NOT_DONE_YET

        return self.response(True,handler,**body['data'])

    def render_GET(self, request):
        self.response.setRequest(request)
        handler = None
        try:
            handler = self.find_handler(request.postpath,self.pages)['action']
        except Exception as e:
            info = self.connectionInfo(request)
            return "Service <b>%s</b> on <b>%s</b>, port <b>%d</b>" % (self.name,info['host'],info['port'])
        return handler(request)
