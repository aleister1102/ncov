import os
import requests
import json
import database as db
import unicodedata
from string import Template

# World API
WORLD_API = 'https://api.covid19api.com/total/country/$name'
WORLD_FILE = '../db/worlds/$name.json'
WORLD_CODE = '../db/codes.json'

# Vietnam API

VIETNAM = 'https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true&utf8=1'
VIETNAM_FILE = '../db/vietnam_specific.json'


def fetchCountry(name):
    '''
    Cập nhật thông tin covid của một quốc gia
     - name: tên quốc gia
    '''

    # Loại bỏ quốc gia bị lỗi

    if(name == 'Saint Vincent and Grenadines'):
        return

    # Lấy API
    response = requests.get(Template(WORLD_API).substitute(name=name))
    if(response.status_code != 200):
        return

    # # Kiểm tra file của nước bất kỳ có tồn tại chưa
    filePath = Template(WORLD_FILE).substitute(name=name)

    string = json.loads(response.content)

    if(string != []):
        print('Fetching', name)
        db.updateJSON(filePath, string)
    else:
        return

    # if(string[0]['Province'] != ""):
    #     print(name," has many provinces")


def fetchWorld():
    '''
    Cập nhật thông tin covid của toàn thế giới và lưu về data base
    - return: True nếu cập nhật thành công, False nếu ngược lại
    '''

    # Nếu đã cập nhật thì return
    if(db.isUpdated()):
        print("World database is already updated")
        return False  # Nếu không có cập nhật

    with open(WORLD_CODE, mode="r") as f:
        worlds = json.load(f)

    print("Fetching World's database")
    # Cập nhật cho từng quốc gia
    for country in worlds:
        fetchCountry(country['country'])
    print("World database is updated")

    return True


def fetchVietnam():
    '''
    Cập nhật thông tin covid các tỉnh thành của Việt Nam trong ngày
    - return: True nếu cập nhật thành công, False nếu ngược lại
    '''

    if(db.isUpdated()):
        print("Vietnam database is already updated")
        return False  # Nếu không có cập nhật

    print("Fetching Vietnam's province")
    # Gọi API
    rq = requests.get(VIETNAM)
    if(rq.status_code != 200):
        return False

    # Lấy dữ liệu và update database
    fetchedData = rq.content
    responseVietnam = json.loads(fetchedData)['locations']
    db.updateJSON(VIETNAM_FILE, responseVietnam)
    print("Vietnam database is updated")

    return True


def fetchData():
    '''
    Cập nhật cơ sở dữ liệu
    '''

    flag = fetchVietnam()
    flag = fetchWorld()
    if(flag == True):
        db.writeLatestTime(db.getCurrentTime())
    print("Fetching is done")


def getCountryData(countryName, date):
    '''
    Lấy dữ liệu của một quốc gia bất kỳ
    - countryName: tên quốc gia
    - date: ngày mong muốn
    - return: dict thông tin nếu tìm thấy, {} nếu không tìm thấy
    '''

    dict = {}
    found = False
    found_time = False
    # Mở file mã thế giới để lấy các tên quốc gia
    with open(WORLD_CODE, mode="r") as f1:
        worlds = json.load(f1)

    print("Searching World's database")
    for country in worlds:
        if(country['country'] == countryName or country['code'] == countryName):
            path = Template(WORLD_FILE).substitute(name=country['country'])
            found = True

            # Có trong danh sách nhưng không có file
            if not os.path.isfile(path):
                print("Cannot find")
                return {}

            # Mở file quốc gia để lấy dữ liệu
            with open(path, mode="r") as f2:
                data = json.load(f2)

    if(found):
        date += "T00:00:00Z"
        for item in data:
            if(item["Date"] == date):
                found_time = True
                return item

    if(found == False or found_time == False):
        print("Cannot find")
        return {}


def unicodeToString(str):
    '''
    Chuyển một chuỗi có unicode thành không dấu
    '''

    return unicodedata.normalize('NFKD', str).encode('ascii', 'ignore').decode('utf-8')


def getProvinceData(provinceName):
    '''
    Lấy dữ liệu của một tỉnh thành bất kỳ
    - provinceName: chuỗi nhập vào có thể là không dấu hoặc có dấu
    - return: dict thông tin nếu tìm thấy, {} nếu không tìm thấy
    '''

    # Chuyển chuỗi đầu vào thành không dấu
    provinceName = unicodeToString(provinceName)

    # Nếu nhập vào Ho Chi Minh thì chuyển thành TP. Ho Chi Minh
    if(provinceName == "Ho Chi Minh"):
        provinceName = "TP. Ho Chi Minh"

    with open(VIETNAM_FILE, mode="r") as f:
        provinces = json.load(f)

    print("Searching Viet Nam's database")
    for province in provinces:
        # Chuyển các chuỗi trong file thành không dấu
        name = unicodeToString(province['name'])
        if(name == provinceName):
            return province

    print("Cannot find")
    return {}


def covidDictToString(dict, option):
    '''
    Hàm chuyển một dictionary thông tin covid thành một chuỗi.
    Muốn thay đổi cách hiển thị thì chỉnh biến str

    - dict: dictionary đầu vào
    - option: tùy chọn xử lý loại thông tin
    - return: "deny" nếu như không tìm thấy thông tin và dict nhận vào là rỗng
    - return: str nếu có thông tin và đã được chuyển thành chuỗi
    '''

    # Không tìm thấy dict sẽ rỗng
    if(dict == {}):
        return "deny"

    # Thông tin của
    if(option == 1):  # thế giới
        str = "Country name: $country\nDates: $date\nConfirmed: $confirmed\nDeaths: $deaths\nRecovered: $recovered\nActive: $active\n"
        str = Template(str).substitute(
            country=dict['Country'], date=dict['Date'], confirmed=dict['Confirmed'], deaths=dict['Deaths'], recovered=dict['Recovered'], active=dict['Active'])
        return str
    elif(option == 2):  # Việt Nam
        str = "Province name: $name\nDeath: $death\nCases: $cases\nToday cases: $casesToday\n"
        str = Template(str).substitute(
            name=dict['name'], death=dict['death'], cases=dict['cases'], casesToday=dict['casesToday'])
        return str
    else:
        return "deny"


''' Cập nhật dữ liệu trước khi chạy, nhớ gọi hàm này sau khi chạy server'''

# fetchData()

''' Đối với thế giới thì dùng Dict to String để lấy chuỗi option 1'''
''' Chuỗi ngày tháng sẽ có dạng như thế này: "2021-12-18"'''

# print(covidDictToString(getCountryData("VN","2021-12-18"),1))

'''Đối với Việt Nam thì dùng Dict to String để lấy chuỗi option 2'''

# covidDictToString(getProvinceData("Ho Chi Minh"), 2)
