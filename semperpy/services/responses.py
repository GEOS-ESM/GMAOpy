#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, May 2010, dev@synopticview.com
#-------------------------------------------------------------------
from twisted.internet import threads, defer, reactor
from twisted.web import http, server

from semperpy.services.response import Response
from semperpy.services.errors import ServiceError

class ImmediateAndBlocking(Response):

    def __call__(self,service,execute,*args,**kargs):
        try:
            result = execute(*args,**kargs)
            self.send_http_response(result,http.OK)
        except Exception as err:
            error = http.INTERNAL_SERVER_ERROR
            if isinstance(err,ServiceError):
                error = err.response_code()
            self.request.setResponseCode(http.OK)
            self.send_http_response(repr(err),error)
        return server.NOT_DONE_YET

class ImmediateAndNonBlocking(Response):

    def success(self,response):
        self.request.setResponseCode(http.OK)
        reactor.callFromThread(self.send_http_response, response, http.OK)

    def failure(self,response):
        error = http.INTERNAL_SERVER_ERROR
        if isinstance(response,ServiceError):
            error = response.response_code()
        self.request.setResponseCode(http.OK)
        reactor.callFromThread(self.send_http_response, response.__str__(), error)

    def __call__(self,service,deferred,*args,**kargs):
        threads.deferToThread(self.execute,deferred,*args,**kargs)
        return server.NOT_DONE_YET

    def execute(self,deferred,*args,**kargs):
        d = defer.maybeDeferred(deferred,*args,**kargs)
        d.addCallback(self.success)
        d.addErrback(self.failure)
