import requests
import json
import database as db


#World
TWO_DAYS_AGO = 'two days ago'
WORLD_TWO_DAYS_AGO = 'https://disease.sh/v3/covid-19/countries?twoDaysAgo=true'
FILE_WORLD2 = 'src/world_two_days_ago.json'

YESTERDAY = 'yesterday'
WORLD_YESTERDAY = 'https://disease.sh/v3/covid-19/countries?yesterday=true'
FILE_WORLD1 = 'src/world_yesterday.json'

WORLD = 'https://disease.sh/v3/covid-19/countries'
FILE_WORLD = 'src/world.json'

#Vietnam

VIETNAM = 'https://disease.sh/vapi.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true'


def fetchCovidWorld(option):
    """
    Fetch Covid information of world.
    option: date
    """

    file = ""
    if(option == TWO_DAYS_AGO):
        responseWorld = requests.get(WORLD_TWO_DAYS_AGO)
        file = FILE_WORLD2
    elif(option == YESTERDAY):
        responseWorld = requests.get(WORLD_YESTERDAY)
        file = FILE_WORLD1
    else:
        responseWorld = requests.get(WORLD)
        file = FILE_WORLD

    Worlds = json.loads(responseWorld.content)
    db.updateJSON(file, Worlds)


def getCovidVietnam(option):
    
    responseVietnam = requests.get(VIETNAM)
    
getCovidVietnam('')


