import requests
import json
import os.path
import database as db
from string import Template


# World API
WORLD_API = 'https://api.covid19api.com/dayone/country/$name/status/confirmed'
WORLD_FILE = 'src/countries/$name.json'
WORLD_CODE = 'src/countries_code.json'

# Vietnam API

VIETNAM = 'https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true&utf8=1'
FILE_VIETNAM = 'src/vietnam/vietnam.json'

# def getCountriesCode():

#     response = json.loads(requests.get(
#         'https://api.covid19api.com/countries').content)
#     list = []
    
#     for country in response:
#         dict = {'country': country['Country'], 'code': country['ISO2']}
#         list.append(dict)
        
#     f = open('src/countries_code.json', 'a')
#     json.dump(list, f, indent=2)


def fetchCountry(name):
    
    print('Fetching',name)
    if(name == 'Saint Vincent and Grenadines'):
        return

    response = requests.get(Template(WORLD_API).substitute(name = name))
    if(response.status_code != 200):
        return
    
    filePath = Template(WORLD_FILE).substitute(name = name)
    if(os.path.isfile(filePath)):
        print('File is existed')
        return
    
    string = json.loads(response.content)
    db.updateJSON(filePath,string)

def fetchWorld():
    
    f = open(WORLD_CODE, 'r')
    worlds = json.load(f)
    
    for country in worlds:
        fetchCountry(country['country'])


def getWorld(name):
    
    pass
 


def fetchVietnam(option):

    responseVietnam = json.loads(requests.get(VIETNAM).content)['locations']
    db.updateJSON(FILE_VIETNAM, responseVietnam)

    # for province in responseVietnam:
    #     if(province['name'] == option):
    #         print(province)


def getVietnam():

    pass




    
    
    
