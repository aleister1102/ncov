import requests
import json
import os.path
import database as db
import datetime
from string import Template




# World API
WORLD_API = 'https://api.covid19api.com/dayone/country/$name/status/confirmed'
WORLD_FILE = 'src/countries/$name.json'
WORLD_CODE = 'src/countries_code.json'

# Vietnam API

VIETNAM = 'https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true&utf8=1'
VIETNAM_FILE = 'src/vietnam_specific.json'

#Time
TIME_FILE = 'src/time.json'

#! Move to database.py
def getCurrentTime():
    
    time = datetime.datetime.now()
    #Trả về một dictionary
    return {'year': time.year, 'month': time.month, 'day':time.day, 
            'hour':time.hour, 'minute':time.minute, 'second':time.second}
    
def readLatestTime():
    
    f = open(TIME_FILE,'r')
    time = json.load(f)
    #Trả về một dictionary cho thời gian gần đây
    return time[-1]

def isUpdated():
    
    latestTime = readLatestTime()
    currentTime = getCurrentTime()
    
    hourDiff = currentTime['hour'] - latestTime['hour']
    minDiff = currentTime['minute'] - latestTime['minute']
    
    if(hourDiff > 1):
        return False
    if(hourDiff == 1):
        if(minDiff >=0):
            return False
        else:
            return True
    else:
        return True
        

    

def fetchCountry(name):
    
    """
    Cập nhật thông tin covid của một quốc gia
    name: tên quốc gia
    """
    #Nếu đã cập nhật thì return
    if(isUpdated()):
        return
    
    #Loại bỏ quốc gia bị lỗi
    print('Fetching',name)
    if(name == 'Saint Vincent and Grenadines'):
        return

    #Lấy API
    response = requests.get(Template(WORLD_API).substitute(name = name))
    if(response.status_code != 200):
        return
    
    #Kiểm tra file của nước bất kỳ có tồn tại chưa
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
    f.close()

def fetchVietnam(option):

    """
    Cập nhật thông tin covid các tỉnh thành của Việt Nam trong một ngày
    option: tên tỉnh thành
    """
    responseVietnam = json.loads(requests.get(VIETNAM).content)['locations']
    db.updateJSON(VIETNAM_FILE, responseVietnam)

    # for province in responseVietnam:
    #     if(province['name'] == option):
    #         print(province)

isUpdated()