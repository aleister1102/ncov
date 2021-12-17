import json
import datetime as dt
from datetime import timedelta as td

# Time
TIME_FILE = '../db/update_time.txt'
ACC_FILE = '../db/accounts.json'

def getCurrentTime():

    time = dt.datetime.now()
    # Trả về một datetime
    return time


def readLatestTime():

    with open(TIME_FILE, encoding='utf8', mode="r") as f:
        timeList = f.readlines()

    # Lấy ngày mới nhất
    strTime = timeList[-1]

    # Nếu dòng cuối rỗng
    if(strTime == ""):
        strTime = timeList[-2]

    # Chuyển về kiểu datetime và trả về
    time = dt.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")
    return time


def writeLatestTime(time):
    """
        time: kiểu datetime
    """

    with open(TIME_FILE, encoding='utf8', mode="a") as f:

        # Chuyển kiểu datetime thành chuỗi
        strTime = dt.datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        f.write('\n')
        f.write(strTime)


def isUpdated():

    # Lấy thời gian mới nhất trong file và hiện tại
    latestTime = readLatestTime()
    currentTime = getCurrentTime()
    delta = currentTime - latestTime

    # Nhiều hơn 1 giờ thì là chưa cập nhật
    if(delta.seconds > 3600):
        return False
    return True


def accountToDict(list):

    account = {
        "username": "",
        "password": ""
    }

    account['username'] = list[0]
    account['password'] = list[1]

    return account


def getAccount():

    with open(ACC_FILE, mode = 'r') as f:
        data = json.load(f)
    return data


def checkAccount(clientAccount):
    """
    Hàm đăng nhập, kiểm tra tài khoản có tồn tại chưa

    clientAccount: list gồm username và password
    return: True nếu như tài khoản tồn tại, cho phép đăng nhập, False nếu ngược lại
    """
    accounts = getAccount()
    for account in accounts:
        if(account['username'] == clientAccount[0] and account['password'] == clientAccount[1]):
            return True

    print("Account is not existed")
    return False


def createAccount(clientAccount):
    """
    Hàm tạo tài khoản

    clientAccount: list gồm username và password
    return: True nếu như tạo tài khoản thành công, False nếu như tạo thất bại
    """

    accounts = getAccount()
    accountDict = accountToDict(clientAccount)
    if(checkAccount(clientAccount) == False):
        accounts.append(accountDict)
        updateJSON(ACC_FILE, accounts)
        print("Create account successfully")
        return True
    else:
        print("Account is existed")
        return False


def updateJSON(file, data):

    with open(file,mode =  "w") as f:
        json.dump(data, f, indent=2)

list = ["2","1"]
createAccount(list)