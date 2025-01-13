#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, April 2010, dev@synopticview.com
#-------------------------------------------------------------------
import time
import urllib.request, urllib.error, urllib.parse

from semperpy.services.errors import *
from semperpy.services.contents import Contents
from semperpy.services.protocol import Protocol

class ServerError(Exception):
    pass

class Client(object):

    def __init__(self, url):
        self.url = url

    def execute(self, data, *args, **kwargs):
        data = Contents.encode(data=data)
        req = urllib.request.Request(self.url,data=data)
        req.add_header("Content-Type", "application/json")

        opener = urllib.request.build_opener(urllib.request.BaseHandler())
        response = opener.open(req)
        dec = response.read()
        value = Contents.decode(dec)
        for key in Protocol.keywords():
            if not key in value:
                raise BadRequest('The %s field is missing in the reply' % (key))
        if value['code'] != 200:
            raise ServerError(value['data'])
        return value['data']
