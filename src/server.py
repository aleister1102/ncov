import socket
import threading
from tkinter.constants import NO
import database as db

# HOST = socket.gethostbyname(socket.gethostname())
HOST = "127.0.0.1"
SERVER_PORT = 52467
FORMAT = "utf8"


def recvList(connection, option):
    '''
    Hàm nhận danh sách từ phía client theo một option cho trước
    - connection: kết nối mà server đã mở với client
    - option: tùy chọn loại thông tin
    '''

    list = []
    item = None
    msgServer = "err"
    # print("option: " + option)
    while(item != "end"):
        item = connection.recv(1024).decode(FORMAT)
        if(item != "end"):
            list.append(item)
        else:
            # In để kiểm tra
            print(list)
            # Nếu option = 1 thì đi đến hàm login
            if(option == 1):
                if(db.checkAccount(list) == True):
                    msgServer = "no-err"
            # nếu option = 0 thì đi đến hàm regis
            elif(option == 0):
                if(db.createAccount(list) == True):
                    msgServer = "no-err"

        # Gửi hồi đáp cho bên client
        connection.sendall(msgServer.encode(FORMAT))
    return msgServer


def handleClient(connection, address):  # Xử lý đa luồng
    '''
    Hàm xử lý đa luồng cho mỗi kết nối của client
    - connection: kết nối của client
    - address: địa chỉ IP và port của client
    '''

    print("Client ", address, " connected !!!")
    print("Connection", connection.getsockname())
    check = True
    temp = "err"
    # msgClient = None
    try:
        while(temp == "err"):

            msgClient = connection.recv(1024).decode(FORMAT)
            # print("Client", address, "says: ", msgClient)
            connection.sendall(msgClient.encode(FORMAT))

            # Nếu nhận được tin "1" thì sẽ sẵn sàng mở hàm nhận tin với option 1
            if(msgClient == "1"):
                temp = recvList(connection, 1)
            # Nếu nhận được tin "0" thì sẽ sẵn sàng mở hàm nhận tin với option 0
            elif(msgClient == "0"):
                temp = recvList(connection, 0)
            elif(msgClient == "check"):
                pass
            else:
                temp = "no-err"

        while(msgClient != "x"):
            msgClient = connection.recv(1024).decode(FORMAT)
            # print("Client", address, "says: ", msgClient)
            connection.sendall(msgClient.encode(FORMAT))

        print("Client: ", address, " finished !!!")
        print(connection.getsockname(), " closed !!!")
        connection.close()

    except:
        check = False
        temp = "err"

    if(check == False):
        print("Client", address, " is disconnected !!!")
        connection.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def openServer():

    print("SERVER SIDE")
    print("Server: ", HOST, SERVER_PORT)
    print("Waiting for Client ...")

    s.bind((HOST, SERVER_PORT))
    s.listen()
    while(1):
        try:
            # type = input()
            # if(type != "x"):
            connection, address = s.accept()
            # handleClient(connection, address)
            thr = threading.Thread(target=handleClient,
                                   args=(connection, address))
            thr.daemon = False
            thr.start()
            # else:
            # print("Server is closed !!!")
            # closeServer(s)
            # break
        except:
            print("Server is closed !!!")
            closeServer(s)
            break


def closeServer(s):
    print("\t--- END SERVER ---")
    s.close()


openServer()
