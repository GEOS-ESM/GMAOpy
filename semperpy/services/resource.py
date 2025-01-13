#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, May 2010, dev@synopticview.com
#-------------------------------------------------------------------
from twisted.web import http, resource

from semperpy.services.html import HTML

class Resource(resource.Resource):

    def __init__(self):
        resource.Resource.__init__(self)

    def unimplemented(self, request):
        request.setResponseCode(http.NOT_ALLOWED)
        return ""

    render_CONNECT = unimplemented
    render_DELETE = unimplemented
    render_GET = unimplemented
    render_HEAD = unimplemented
    render_OPTIONS = unimplemented
    render_POST = unimplemented
    render_PUT = unimplemented
    render_TRACE = unimplemented

    def connectionInfo(self,request):
        info = {}
        info['host'] = request.getRequestHostname()
        info['port'] = request.getHost().port
        info['title'] = "services on host: %s, port %d" % (info['host'],info['port'])
        return info

    def name(self):
        raise SystemError('method not implemented')

    def html(self,request):
        return ""
