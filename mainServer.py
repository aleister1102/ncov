import socket
import threading


HOST = socket.gethostbyname(socket.gethostname())

SERVER_PORT = 52467
FORMAT = "utf8"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")

print("Server: ", HOST, SERVER_PORT)
print("Waiting for Client ...")


def recvList(connection):
    list = []
    item = None
    msgServer = "Server received the messages !!!"
    while(item != "end"):
        item = connection.recv(1024).decode(FORMAT)
        if(item != "end"):
            list.append(item)
        # Server response
        connection.sendall(msgServer.encode(FORMAT))

    return list


def handleClient(connection, address):  # Xử lý đa luồng
    print("Client ", address, " connected !!!")
    print("Connection", connection.getsockname())

    msgClient = None
    msgServer = None
    type = None

    check = True
    while(msgClient != "x"):
        try:
            msgClient = connection.recv(1024).decode(FORMAT)
            print("Client", address, "says: ", msgClient)
            msgServer = "Server received the messages !!!"
            connection.sendall(msgServer.encode(FORMAT))

            if(msgClient == "list"):
                list = recvList(connection)
                print(list)

        except:
            check = False
            msgClient = "x"

    if(check == True):
        print("Client: ", address, " finished !!!")
        print(connection.getsockname(), " closed !!!")
        connection.close()
        type = input()
        if(type == "x"):
            s.close()
            exit(1)

    else:
        print("Client", address, " is disconnected !!!")
        connection.close()


while(1):

    try:
        connection, address = s.accept()
        thr = threading.Thread(target=handleClient, args=(connection, address))
        thr.daemon = False
        thr.start()

    except:
        print("Server is closed !!!")
        break


print("\t--- END SERVER ---")
s.close()
