from semperpy.services.server import Server
from semperpy.services.errors import ServiceError

def add(args):
    return sum(args)

def diff(args):
    if len(args) > 2 or len(args) <= 1:
        raise ServiceError('only two arguments are accepted for the difference')
    return args[0] - args[1]

def calculate(operator,arguments):
    if operator == '+':
        return sum(arguments)
    elif operator == '-':
        return diff(arguments)
    else:
        raise ServiceError("Unknow operator '%s'" % operator)

Server.registerService("calculate",calculate)
server = Server()
server.run(port=8880)
