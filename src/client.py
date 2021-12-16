import time
import socket


HOST = "127.0.0.1"
SERVER_PORT = 52467
FORMAT = "utf8"

# Hàm gửi list


def sendList(client, list):
    msgServer = None
    list.append("end")
    for item in list:
        client.sendall(item.encode(FORMAT))
        # Wait response from server
        msgServer = client.recv(1024).decode(FORMAT)

    return msgServer

# Hàm gửi các yêu cầu cụ thể, nếu không đn hoặc đk thì truyền vào list = []


def sendOption(client, msgClient, list):
    # Gửi option và kiểm tra có gửi được không
    client.sendall(msgClient.encode(FORMAT))
    msgServer = client.recv(1024).decode(FORMAT)
    # Server phản hồi lại khác thì chưa gửi được
    if(msgServer != msgClient):
        return
    if(msgClient == "1" and list != []):
        check = sendList(client, list)
        if(check == "TRUE"):
            print("Login successed !!!")

        else:
            print("Login failed !!!")

    elif(msgClient == "0" and list != []):
        check = sendList(client, list)
        if(check == "TRUE"):
            print("Register successed !!!")

        else:
            print("Register failed !!!")
# Chờ time out


def waitTO(client):
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

# Mở kết nối


def connectToServer():

    # Tạo kết nối
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("CLIENT SIDE")
        # Chờ time out
        check = waitTO(client)
        if(check != 0):
            print("Time Out !!!")
            closeConnection(client)
        # Trả về tiếp tục dùng cho việc khác
        else:
            return client
    except:

        print("ERROR !!!")
        print("Server is disconnected !!!")
        closeConnection(client)

# Đóng kết nối


def closeConnection(client):
    client.close()


list1 = ["20120356", "2"]
list2 = ["20120356", "2"]
list3 = ["20120356", "2"]
list4 = ["20120356", "1"]
client = connectToServer()
sendOption(client, "1", list1)
sendOption(client, "1", list2)
sendOption(client, "1", list3)
sendOption(client, "1", list4)
