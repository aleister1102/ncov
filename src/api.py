import requests
import json
import os.path
import database as db
from string import Template


# World API
TWO_DAYS_AGO = 'two days ago'
WORLD_TWO_DAYS_AGO = 'https://disease.sh/v3/covid-19/countries?twoDaysAgo=true'
FILE_WORLD2 = 'src/world_two_days_ago.json'

YESTERDAY = 'yesterday'
WORLD_YESTERDAY = 'https://disease.sh/v3/covid-19/countries?yesterday=true'
FILE_WORLD1 = 'src/world_yesterday.json'

TODAY = 'today'
WORLD = 'https://disease.sh/v3/covid-19/countries'
FILE_WORLD = 'src/world.json'

# Vietnam API

VIETNAM = 'https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true&utf8=1'
FILE_VIETNAM = 'src/vietnam.json'

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
    
    print('fetching',name)
    if(name == 'Saint Vincent and Grenadines'):
        return
    try:
        response = requests.get(Template('https://api.covid19api.com/dayone/country/$name/status/confirmed').substitute(name = name))
        if(response.status_code != 200):
            return
        
        string = json.loads(response.content)
        db.updateJSON(Template('src/countries/$name.json').substitute(name = name),string)
    except:
        return

def fetchWorld():
    """
    Fetch Covid information of world.
    option: date
    """

    f = open('src/countries_code.json', 'r')
    worlds = json.load(f)
    
    for country in worlds:
        fetchCountry(country['country'])

def getWorld(option):
    
    f = open('src/countries_code.json', 'r')
    worlds = json.load(f)
    i = 0
    for country in worlds:
        i+=1
        print(i)
        print(country)


def fetchVietnam(option):

    responseVietnam = json.loads(requests.get(VIETNAM).content)['locations']
    db.updateJSON(FILE_VIETNAM, responseVietnam)

    for province in responseVietnam:
        if(province['name'] == option):
            print(province)


def getVietnam():

    file = open(FILE_VIETNAM, 'r')
    return json.load(file)


fetchWorld()

    
    
    
