import time
import socket


SERVER_PORT = 52467

CLIENT_PORT = 8001
FORMAT = "utf8"

#HOST = input("Input Server's IP: ")

HOST = "192.168.1.13"


def sendList(client, list):
    msgServer = None
    list.append("end")
    for item in list:
        client.sendall(item.encode(FORMAT))
        # Wait response from server
        msgServer = client.recv(1024).decode(FORMAT)

    return msgServer


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind((HOST, CLIENT_PORT))

print("CLIENT SIDE")

try:

    connect = 0
    connectTime = 0
    check = client.connect_ex((HOST, SERVER_PORT))
    while(connectTime <= 10 and check != 0):
        if(connect == 0):
            print("Waiting for Server open the connection ...")
            connect = 1

        check = client.connect_ex((HOST, SERVER_PORT))
        if(check == 0):
            break
        connectTime += 1
        time.sleep(1)

    if(check == 0):
        print("Client address: ", client.getsockname())

        list = ["LePhuocToan", "20120386"]

        msgClient = None
        msgServer = None

        while(msgClient != "x"):
            msgClient = input("Client talks somethings: ")
            client.sendall(msgClient.encode(FORMAT))
            client.recv(1024).decode(FORMAT)
            if(msgClient == "SIGN IN"):
                msgServer = sendList(client, list)
                print(msgServer)

            else:
                print(msgServer)

        client.close()
    else:
        print("Time out")
        client.close()

except:
    print("ERROR !!!")
    print("Server is disconnected !!!")
    client.close()
