#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, April 2010, dev@synopticview.com
#-------------------------------------------------------------------
import sys

from twisted.web import http

class ServiceError(Exception):
    
    def __init__(self,message=""):
        super(Exception,self).__init__()
        self.message = message
        self.type, self.value, self.tb = sys.exc_info()

    def __str__(self):
        return self.message

    def to_dict(self):
        return { 'data': self.__str__() }

    def response_code(self):
        return http.INTERNAL_SERVER_ERROR

class CommunicationError(ServiceError):
    """
        any low level communication error
    """


class BadRequest(ServiceError):
    """
        errors due to data encoding, unknown content
    """
    def response_code(self):
        return http.BAD_REQUEST
