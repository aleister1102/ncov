import json

def listToDict(list):

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

    for account in data['account']:
        if(account['username'] == clientAccount['username'] and account['password'] == clientAccount['password']):
            return True

    print('False')
    return False


def createAccount(clientAccount):

    data = getAccount()
    clientAccount = listToDict(clientAccount)
    if(checkAccount(data, clientAccount) == False):
        data['account'].append(clientAccount)
    else:
        return False
    
    return True


def updateJSON(file, data):
    
    f = open(file, 'w')
    json.dump(data, f, indent=2)
    f.close()

