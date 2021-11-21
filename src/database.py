import json

def accountToDict(list):

    account = {
        "username": "",
        "password": ""
    }

    account['username'] = list[0]
    account['password'] = list[1]

    return account


def getAccount():

    f = open('accounts.json', 'r')
    data = json.load(f)
    f.close()
    return data


def printAccount(data):

    for account in data['account']:
        print(account)


def checkAccount(data, clientAccount):

    """
    Hàm đăng nhập, kiểm tra tài khoản có tồn tại chưa
    data: dữ liệu tên đăng nhập từ database, lấy bằng hàm getAccount()
    clientAccount: list gồm username và password
    return: True nếu như tài khoản tồn tại, cho phép đăng nhập, False nếu ngược lại
    """
    
    for account in data['account']:
        if(account['username'] == clientAccount['username'] and account['password'] == clientAccount['password']):
            return True

    print('False')
    return False


def createAccount(clientAccount):

    """
    Hàm tạo tài khoản
    clientAccount: list gồm username và password
    return: True nếu như tạo tài khoản thành công, False nếu như tạo thất bại
    """
    
    data = getAccount()
    clientAccount = accountToDict(clientAccount)
    if(checkAccount(data, clientAccount) == False):
        data['account'].append(clientAccount)
    else:
        return False
    
    return True


def updateJSON(file, data):
    
    f = open(file, 'w')
    json.dump(data, f, indent=2)
    f.close()

