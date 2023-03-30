import requests

print(requests.get(r'http://127.0.0.1:8080/rest/notes/1').json())
