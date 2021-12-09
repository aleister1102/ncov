import requests
import json
import database as db
from string import Template

# World API
WORLD_API = 'https://api.covid19api.com/dayone/country/$name/status/confirmed'
WORLD_FILE = '../db/worlds/$name.json'
WORLD_CODE = '../db/codes.json'

# Vietnam API

VIETNAM = 'https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true&utf8=1'
VIETNAM_FILE = '../db/vietnam_specific.json'


def fetchCountry(name):
    """
    Cập nhật thông tin covid của một quốc gia
    name: tên quốc gia
    """

    # Loại bỏ quốc gia bị lỗi
    print('Fetching', name)
    if(name == 'Saint Vincent and Grenadines'):
        return

    # Lấy API
    response = requests.get(Template(WORLD_API).substitute(name=name))
    if(response.status_code != 200):
        return

    # # Kiểm tra file của nước bất kỳ có tồn tại chưa
    filePath = Template(WORLD_FILE).substitute(name=name)
    # if(os.path.isfile(filePath)):
    #     print('File is existed')
    #     return

    string = json.loads(response.content)
    db.updateJSON(filePath, string)


def fetchWorld():
    """
    Cập nhật thông tin covid của toàn thế giới và lưu về data base
    """

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
    """
    Cập nhật thông tin covid các tỉnh thành của Việt Nam trong ngày
    """

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
    flag = fetchVietnam()
    flag = fetchWorld()
    if(flag == True):
        db.writeLatestTime(db.getCurrentTime())
    print("Fetching is done")


def getCountryData(countryName):

    with open(WORLD_CODE, mode="r") as f:
        worlds = json.load(f)

    print("Searching World's database")
    for country in worlds:
        if(country['country'] == countryName):
            path = Template(WORLD_FILE).substitute(name=countryName)
            with open(path, mode='r') as f:
                data = json.load(f)
                # Đảo ngược danh sách cho ngày mới nhất lên đầu
                return data.reverse()

    print("Cannot find")
    return []


def getProvinceData(province):

    with open(VIETNAM_FILE, mode="r") as f:
        provinces = json.load(f)

    for province in provinces:
        # Tên tỉnh phải có dấu
        if(province['name'] == province):
            path = VIETNAM_FILE
            with open(path, mode='r') as f:
                data = json.load(f)
                return data

    print("Cannot find")
    return []


def covidDictToString(dict, option):
    """
        Hàm chuyển một dictionary thông tin covid thành một chuỗi.
        Muốn thay đổi cách hiển thị thì chỉnh biến str

        dict: dictionary đầu vào
    """

    # Thông tin của
    if(option == 1):  # thế giới
        str = "Country name: $name\nDates: $date\nCases: $cases\n"
        str = Template(str).substitute(
            name=dict['Country'], date=dict['Date'], cases=dict['Cases'])
        return str
    elif(option == 2): #Việt Nam
        str = "Province name: $name\nDeath: $death\nCases: $cases\nToday cases: $casesToday\n"
        str = Template(str).substitute(
            name=dict['name'], death=dict['death'], cases=dict['cases'], casesToday=dict['casesToday'])
        return str

    return ""

fetchData()
