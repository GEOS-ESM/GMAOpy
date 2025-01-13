from semperpy.services.server import Server

def add(args):
    return sum(args)

def diff(args):
    return args[0] - args[1]

def calculate(operator,arguments):
    operators = { '+': add, '-': diff }
    return operators[operator](arguments)

Server.registerService("calculate",calculate)
server = Server()
server.run(port=8880)
