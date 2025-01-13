from semperpy.services.server import Server

def execute(a,b):
    print(a,b)
    return {'greeting':'hello','number':42}

def info(request):
    return "Hello, I am here"

def status(request):
    return "Hello, this is my status"

def ping(request):
    return "ping"

def refined(request):
    return "Hello, this is refined"

def other(request):
    return "Hello, this is other"

Server.registerService('retrieve',execute)
Server.registerPage('retrieve',info)
Server.registerPage(['retrieve','status'],status)
Server.registerPage(['retrieve','ping','refined'],refined)
Server.registerPage(['retrieve','ping','refined','other'],other)
Server.registerPage(['retrieve','ping'],ping)
server = Server()
server.run(port=8880)
