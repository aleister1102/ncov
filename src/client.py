import time
import socket


SERVER_PORT = 52467

FORMAT = "utf8"

# HOST = input("Input Server's IP: ")

HOST = "192.168.198.1"

print("CLIENT SIDE")


def inputIP():
    HOST = input("Input Server's IP: ")

    return HOST


def sendList(client, list):
    msgServer = None
    list.append("end")
    for item in list:
        client.sendall(item.encode(FORMAT))
        # Wait response from server
        msgServer = client.recv(1024).decode(FORMAT)

    return msgServer


def checkList(client, check):
    if(check == 0):
        print("Client address: ", client.getsockname())

        # Nếu có hàm lấy sự kiện từ giao diện thì nếu bấm login sẽ trả về 0
        # Bấm Regis sẽ trả về 1
        msgClient = input("Client talks somethings: ")
        client.sendall(msgClient.encode(FORMAT))
        client.recv(1024).decode(FORMAT)

        if(msgClient != "x"):
            list = ["LePhuocToan", "20120386"]
            msgServer = None

            if(msgClient == "1"):
                msgServer = sendList(client, list)
                if(msgServer == "TRUE"):
                    print("Login successed !!!")

                else:
                    print("Login failed !!!")

            elif(msgClient == "0"):
                msgServer = sendList(client, list)
                if(msgServer == "TRUE"):
                    print("Register successed !!!")

                else:
                    print("Register failed !!!")

        else:
            closeConnection(client)


# Trả về socket Client
def createConnection():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client


def closeConnection(client):
    client.close()


def connectToServer(client):
    try:
        connect = 0
        connectTime = 0

        check = client.connect_ex((HOST, SERVER_PORT))
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
    except:

        print("ERROR !!!")
        print("Server is disconnected !!!")
        closeConnection(client)


def openConnection(client):
    try:
        check = connectToServer(client)
        if(check == 0):
            checkList(client, check)
        else:
            print("Time Out !!!")
            closeConnection(client)
    except:
        print("ERROR !!!")
        print("Server is disconnected !!!")
        closeConnection(client)


client = createConnection()
openConnection(client)
closeConnection(client)
