from semperpy.services.server import Server

def help(*args):
    return """
    <head>
    <title>
        "Calculator, help"
    </title>
    </head>
    <body>
        <h1>Help for the service calculate</h1>
        <p>In order to use the calculator....</p>
    </body>
    """

Server.registerPage("calculate",help)
server = Server()
server.run(port=8880)
