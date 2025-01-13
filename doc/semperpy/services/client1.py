from semperpy.services.client import Client

client = Client("http://localhost:8880/calculate")
print(client.execute({'operator': '+', 'arguments': [12,8,3]}))
