import requests
import json
import database as db
from string import Template

# World API
WORLD_API = 'https://api.covid19api.com/dayone/country/$name/status/confirmed'
#WORLD_FILE = '../db/worlds/$name.json'
WORLD_FILE = 'C:/Users/rongc/OneDrive - VNU-HCMUS/Desktop/Study/Code/MMT/ncov-20CTT3/db/worlds/$name.json'
#WORLD_CODE = '../db/codes.json'
WORLD_CODE = r'C:\Users\rongc\OneDrive - VNU-HCMUS\Desktop\Study\Code\MMT\ncov-20CTT3\db\codes.json'

# Vietnam API

VIETNAM = 'https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true&utf8=1'
#VIETNAM_FILE = '../db/vietnam_specific.json'
VIETNAM_FILE = r'C:\Users\rongc\OneDrive - VNU-HCMUS\Desktop\Study\Code\MMT\ncov-20CTT3\db\vietnam_specific.json'


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
<<<<<<< Updated upstream
            with open(path, mode='r') as f:
                data = json.load(f)
                # Đảo ngược danh sách cho ngày mới nhất lên đầu
                return data.reverse()
=======

            # Mở file quốc gia để lấy dữ liệu
            with open(path, mode="r") as f2:
                data = json.load(f2)
                # Đảo ngược để ngày mới nhất lên đầu và cho vào list
                for item in reversed(data):
                    list.append(item)
                newlist = dict(list[0])
                return newlist
>>>>>>> Stashed changes

    print("Cannot find")
    return []


def getProvinceData(province):

    with open(VIETNAM_FILE, mode="r") as f:
        provinces = json.load(f)

    for province in provinces:
<<<<<<< Updated upstream
        # Tên tỉnh phải có dấu
        if(province['name'] == province):
            path = VIETNAM_FILE
            with open(path, mode='r') as f:
                data = json.load(f)
                return data

    print("Cannot find")
    return []
=======
        # Chuyển các chuỗi trong file thành không dấu
        name = unicodeToString(province['name'])
        if(name == provinceName):
            print(province)
            return province
    print("Cannot find")
    return {}


def unicodeToString(str):
    '''
    Chuyển một chuỗi có unicode thành không dấu
    '''

    return unicodedata.normalize('NFKD', str).encode('ascii', 'ignore').decode('utf-8')


def covidListToString(list):
    '''
    Chuyển một list dữ liệu thành string
    - list: list dữ liệu cần chuyển
    - return: chuỗi thông tin, không tìm thấy thì trả về "deny"
    '''

    # Không tìm thấy list sẽ rỗng
    if(list == []):
        return "deny"

    else:
        """"""
        info = ""
        for item in list:
            info += covidDictToString(item, 1)
        
        print(info)
        return info
>>>>>>> Stashed changes


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

<<<<<<< Updated upstream
fetchData()
=======
''' Cập nhật dữ liệu trước khi chạy, nhớ gọi hàm này sau khi chạy server'''

# fetchData()

''' Trường hợp tìm thấy '''

# Đối với thế giới thì dùng List to String để lấy chuỗi

#covidDictToString(getCountryData("Viet Nam"),1)
#print(getCountryData("Viet Nam"))

# Đối với Việt Nam thì dùng Dict to String để lấy chuỗi

#covidDictToString(getProvinceData("Ho Chi Minh"), 2)

''' Trường hợp không tìm thấy'''

# print(covidListToString(getCountryData("asdasd")))
# print(covidDictToString(getProvinceData("Ha Noi"), 2))

>>>>>>> Stashed changes
