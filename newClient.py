import socket
import time

SERVER_PORT = 52467

CLIENT_PORT = 8001
FORMAT = "utf8"

HOST = input("Input Server's IP: ")


def sendList(client, list):
    msgServer = None
    for item in list:
        client.sendall(item.encode(FORMAT))
        # Wait response from server
        msgServer = client.recv(1024).decode(FORMAT)

    print(msgServer)
    msg = "end"
    client.sendall(msg.encode(FORMAT))


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

        list = ["LePhuocToan", "20120386", "20CTT3"]

        msgClient = None
        msgServer = None

        while(msgClient != "x"):
            msgClient = input("Client talks somethings: ")
            client.sendall(msgClient.encode(FORMAT))
            if(msgClient == "list"):
                client.recv(1024).decode(FORMAT)
                sendList(client, list)
            else:
                msgServer = client.recv(1024).decode(FORMAT)
                print(msgServer)

        client.close()
    else:
        print("Time out")
        client.close()

except:
    print("ERROR !!!")
    print("Server is disconnected !!!")
    client.close()
