import urllib.request, urllib.error, urllib.parse
from semperpy.services.client import Client

client = Client("http://localhost:8880/retrieve")
result = client.execute({'a': 12, 'b': 'Hello'})
print(result)
print(result)
