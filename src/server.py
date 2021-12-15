import socket
import threading


HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 52467
FORMAT = "utf8"


print("SERVER SIDE")

print("Server: ", HOST, SERVER_PORT)
print("Waiting for Client ...")


def checkAccount(clientAccount):
    return True


def createAccount(clientAccount):
    return True


# Nếu option = 1 thì đi đến hàm login
# nếu option = 0 thì đi đến hàm regis
def recvList(connection, option):
    list = []
    item = None
    msgServer = "FALSE"
    while(item != "end"):
        item = connection.recv(1024).decode(FORMAT)
        if(item != "end"):
            list.append(item)
        else:
            # In để kiểm tra
            print(list)
            if(option == 1):
                if(checkAccount(list) == True):
                    msgServer = "TRUE"
            else:
                if(createAccount(list) == True):
                    msgServer = "TRUE"
        # Gửi hồi đáp cho bên client
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
            # Nếu nhận được tin "1" thì sẽ sẵn sàng mở hàm nhận tin với option 1
            # Nếu nhận được tin "0" thì sẽ sẵn sàng mở hàm nhận tin với option 0
            if(msgClient == "1"):
                recvList(connection, 1)
            elif(msgClient == "0"):
                recvList(connection, 0)

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


def createServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s


def openServer():
    s = createServer()
    s.bind((HOST, SERVER_PORT))
    s.listen()
    while(1):
        try:
            type = input()
            if(type != "x"):
                connection, address = s.accept()
                thr = threading.Thread(target=handleClient,
                                       args=(connection, address))
                thr.daemon = False
                thr.start()
            else:
                print("Server is closed !!!")
                closeServer(s)
                break
        except:
            print("Server is closed !!!")
            closeServer(s)
            break


def closeServer(s):
    print("\t--- END SERVER ---")
    s.close()


openServer()
