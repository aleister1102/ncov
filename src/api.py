import requests
import json
import database as db

response = requests.get(' https://coronavirus-19-api.herokuapp.com/all')
vietnam = requests.get(
    'https://coronavirus-19-api.herokuapp.com/countries/{vietnam}')

data = json.loads(vietnam.content)
print(data)



