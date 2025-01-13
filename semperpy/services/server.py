#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, May 2010, dev@synopticview.com
#-------------------------------------------------------------------
from twisted.internet import reactor
from twisted.web import http, server, resource
from twisted.web.static import File

from semperpy.core.tools import to_list, is_dict
from semperpy.services.contents import Contents
from semperpy.services.errors import ServiceError
from semperpy.services.resource import Resource
from semperpy.services.responses import ImmediateAndNonBlocking
from semperpy.services.service import Service
from semperpy.services.html import HTML

class Server(Resource):

    services = {}
    pages = {}

    def __init__(self,response=ImmediateAndNonBlocking()):
        Resource.__init__(self)
        s = set(self.services.keys())
        s = s.union(list(self.pages.keys()))
        for service in s:
            pages = None
            services = None
            if service in self.pages:
                pages = self.pages[service]    
            if service in self.services:
                services = self.services[service]
            s = Service(service,services,pages,response)
            self.putChild(service,s)
            s.putChild('',s)
        self.putChild('',self)
        self.putChild('css',File(HTML.cssPath()))

    def nested(self,request,all,prefix = ""):
        services = []
        for page,links in list(all.items()):
            if is_dict(links):
                items = []
                sub = list(links.keys())
                sub.sort()
                for name in sub:
                    if name != 'action':
                        items.append('<a href="%s/%s">%s</a>' % (prefix+'/'+page,name,name))
                    if is_dict(links[name]):
                        items.append(self.nested(request,links[name],prefix+'/'+page+'/'+name))
                services.append('<a href="%s">%s</a>' % (prefix+'/'+page,page))
                if len(items) > 0:
                    services.append(items)
        return services

    def render_GET(self, request):
        info = self.connectionInfo(request)
        info['actions'] = HTML.list(self.nested(request,self.services))
        info['pages'] = HTML.list(self.nested(request,self.pages))
        info['content'] = HTML.substituteVariables('server',**info)
        return HTML.substituteVariables('body',**info)

    def run(self,port=8080):
        reactor.listenTCP(port,server.Site(self))
        reactor.run()

    @classmethod
    def registerService(self,service,object):
        max = 5
        service = to_list(service)
        if len(service) == 0 or len(service) > max:
            raise ValueError('A minimum of one service level and a maximum of %d service levels are required, %d levels were provided: %s' % (max,len(service),repr(service)))
        self.register(self.services,service,object)

    @classmethod
    def registerPage(self,service,object):
        max = 5
        service = to_list(service)
        if len(service) == 0 or len(service) > max:
            raise ValueError('A minimum of one service level and a maximum of %d service levels are required, %d levels were provided: %s' % (max,len(service),repr(service)))
        self.register(self.pages,service,object)

    @classmethod
    def register(self,where,service,object):
        if not service[0] in where:
            where[service[0]] = {}
        if len(service) > 1:
            self.register(where[service[0]],service[1:],object)
        else:
            where[service[0]]['action'] = object
