import requests
import json
import database as db


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


def fetchWorldCovid(option):
    """
    Fetch Covid information of world.
    option: date
    """

    filePath = ""
    if(option != TODAY):
        return
    if(option == TWO_DAYS_AGO):
        responseWorld = requests.get(WORLD_TWO_DAYS_AGO)
        filePath = FILE_WORLD2
    if(option == YESTERDAY):
        responseWorld = requests.get(WORLD_YESTERDAY)
        filePath = FILE_WORLD1
    else:
        responseWorld = requests.get(WORLD)
        filePath = FILE_WORLD

    Worlds = json.loads(responseWorld.content)
    db.updateJSON(filePath, Worlds)


def getWorldCovid(option):

    filePath = ""
    if(option == TWO_DAYS_AGO):
        filePath = FILE_WORLD2
    elif(option == YESTERDAY):
        filePath = FILE_WORLD1
    else:
        filePath = FILE_WORLD

    file = open(filePath, "r")
    return json.load(file)


def fetchVietnamCovid(option):

    responseVietnam = json.loads(requests.get(VIETNAM).content)['locations']
    db.updateJSON(FILE_VIETNAM, responseVietnam)
    
    for province in responseVietnam:
        if(province['name'] == option):
            print(province)

            
def getVietnamCovid():

    file = open(FILE_VIETNAM, 'r')
    return json.load(file)


# fetchVietnamCovid('')
print(getVietnamCovid())
