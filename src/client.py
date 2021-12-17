import time
import socket


HOST = "127.0.0.1"
SERVER_PORT = 52467
FORMAT = "utf8"


def checkConnection(client):
    '''
    Hàm kiểm tra xem server có bị mất kết nối đột ngột hay không
    - client: connection của client
    - return: True nếu server còn sống, False nếu bị ngắt
    '''
    try:
        client.sendall("check".encode(FORMAT))
        client.recv(1024).decode(FORMAT)
        return True
    except:
        print("Server is not running")
        return False


def sendList(client, list):
    '''
    Hàm gửi danh sách
    - client: kết nối của client
    - list: danh sách cần gửi
    - return: "TRUE" hoặc "FALSE"
    '''
    msgServer = None
    list.append("end")
    for item in list:
        client.sendall(item.encode(FORMAT))
        # Chờ phản hồi từ server
        msgServer = client.recv(1024).decode(FORMAT)
   # msgServer = client.recv(1024).decode(FORMAT)
    return msgServer


def sendOption(client, msgClient, list):
    '''
    Hàm gửi một yêu cầu cụ thể đến server
    - client: kết nối của client
    - msgClient: yêu cầu (option) của client
    - list: danh sách gửi kèm nếu có, không có thì truyền vào rỗng
    '''

    # Kiểm tra xem server có bị mất kết nối đột ngột không
    if(checkConnection(client) == False):
        return

    # Gửi option và kiểm tra có gửi được không
    client.sendall(msgClient.encode(FORMAT))
    msgServer = client.recv(1024).decode(FORMAT)

    # Server phản hồi lại khác thì chưa gửi được
    if(msgServer != msgClient):
        return

    # Xử lý các option
    # option 1 là login
    if(msgClient == "1" and list != []):
        check = sendList(client, list)
        if(check == "TRUE"):
            print("Login successed !!!")
            return True

        else:
            print("Login failed !!!")
            return False

    # option 2 is register
    elif(msgClient == "0" and list != []):
        check = sendList(client, list)
        if(check == "TRUE"):
            print("Register successed !!!")
            return True

        else:
            print("Register failed !!!")
            return False


def waitTO(client):
    '''
    Hàm chờ server mở kết nối
    - client: kết nối đã mở của client
    - return: 0 nếu kết nối thành công, 1 nếu quá timeout
    '''
    connect = 0
    connectTime = 0
    check = client.connect_ex((HOST, SERVER_PORT))
    print("Client address: ", client.getsockname())

    # Vòng lặp chờ Server mở kết nối
    while(connectTime <= 10 and check != 0):
        if(connect == 0):
            print("Waiting for Server open the connection ...")
            connect = 1

        check = client.connect_ex((HOST, SERVER_PORT))

        if(check == 0):
            break

        connectTime += 1
        time.sleep(1)

    return check


def connectToServer():
    '''
    Hàm mở kết nối đến server
    - return: một kết nối nếu kết nối thành công đến server
    '''
    # Tạo kết nối
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("CLIENT SIDE")
        # Chờ time out
        check = waitTO(client)
        if(check != 0):
            print("Time Out !!!")
        else:
            return client
    except:
        print("ERROR !!!")
        print("Server is not opened !!!")
        closeConnection(client)


def closeConnection(client):
    '''
    Hàm đóng kết nối bên phía client
    - client: kết nối của client
    '''
    print("out")
    option = "x"
    client.sendall(option.encode(FORMAT))
    client.close()


"""
list1 = ["20120356", "2"]

client = connectToServer()
sendOption(client, "1", list1)
sendOption(client, "1", list2)
sendOption(client, "x", list2)

"""
