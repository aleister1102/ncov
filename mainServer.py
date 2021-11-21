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


def checkAccount(clientAccount):
    return True


def createAccount(clientAccount):
    return True


def recvListLogin(connection):

    list = []
    item = None
    msgServer = "FALSE"
    while(item != "end"):
        item = connection.recv(1024).decode(FORMAT)
        if(item != "end"):
            list.append(item)
        else:
            print(list)
            if(checkAccount(list) == True):
                msgServer = "TRUE"
        # Server response
        connection.sendall(msgServer.encode(FORMAT))


def recvListRegister(connection):

    list = []
    item = None
    msgServer = "FALSE"
    while(item != "end"):
        item = connection.recv(1024).decode(FORMAT)
        if(item != "end"):
            list.append(item)
        else:
            print(list)
            if(createAccount(list) == True):
                msgServer = "TRUE"
        # Server response
        connection.sendall(msgServer.encode(FORMAT))


def handleClient(connection, address):  # Xử lý đa luồng

    print("Client ", address, " connected !!!")
    print("Connection", connection.getsockname())

    msgClient = None

    check = True
    while(msgClient != "x"):
        try:
            msgClient = connection.recv(1024).decode(FORMAT)
            print("Client", address, "says: ", msgClient)
            connection.sendall(msgClient.encode(FORMAT))

            if(msgClient == "SIGN IN"):
                recvListLogin(connection)

            elif(msgClient == "SIGN UP"):
                recvListRegister(connection)

        except:
            check = False
            msgClient = "x"

    if(check == True):
        print("Client: ", address, " finished !!!")
        print(connection.getsockname(), " closed !!!")
        connection.close()

    else:
        print("Client", address, " is disconnected !!!")
        connection.close()


def openServer(s):

    while(1):
        try:
            connection, address = s.accept()
            thr = threading.Thread(target=handleClient,
                                   args=(connection, address))
            thr.daemon = False
            thr.start()

        except:
            print("Server is closed !!!")
            break


def closeServer(s):
    print("\t--- END SERVER ---")
    s.close()


openServer(s)
