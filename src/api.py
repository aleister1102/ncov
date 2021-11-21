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
FILE_VIETNAM = 'src/vietnam_specific.json'

def fetchCountry(name):
    
    """
    Cập nhật thông tin covid của một quốc gia
    name: tên quốc gia
    """
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
    
    """
    Cập nhật thông tin covid của toàn thế giới và lưu về data base
    """
    f = open(WORLD_CODE, 'r')
    worlds = json.load(f)
    
    for country in worlds:
        fetchCountry(country['country'])

def fetchVietnam(option):

    """
    Cập nhật thông tin covid các tỉnh thành của Việt Nam trong một ngày
    option: tên tỉnh thành
    """
    responseVietnam = json.loads(requests.get(VIETNAM).content)['locations']
    db.updateJSON(FILE_VIETNAM, responseVietnam)

    # for province in responseVietnam:
    #     if(province['name'] == option):
    #         print(province)




    
    
