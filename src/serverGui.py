import tkinter as tk
from tkinter import  StringVar, messagebox
from tkinter import ttk
import re
import socket
import threading


HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 52467
FORMAT = "utf8"

#Đóng gói hàm lại, không gọi hàm ở ngoài như thế này
window = tk.Tk()

window.title("nCovi_server")
window.iconbitmap(r'C:\Users\rongc\OneDrive - VNU-HCMUS\Desktop\Study\Code\MMT\ncov-20CTT3\imgs\logo.ico')
window.geometry("720x480")
window.resizable(width=False, height=False)

frame2 = tk.Frame(window, highlightbackground="green", highlightthickness=3)
frame1 = tk.Frame(window, highlightbackground="red", highlightthickness=3)
frame3 = tk.Frame(window, highlightbackground="blue", highlightthickness=3)

# kiểm tra đăng nhập
def check_login():
    account = []

    username = entry_username.get()
    password = entry_password.get()

    account.append(username) 
    account.append(password)

    if(username == "" or password == "" ):
        messagebox.showinfo("", "Blank not allowed")
    elif (len(username) >= 30) or (len(password) >= 30):
        messagebox.showinfo("","Too much character" + "\n" + "The username or password must less than 30 character")
    elif not (re.match("^[a-zA-Z0-9]*$",username) and re.match("^[a-zA-Z0-9]*$",password)):
         messagebox.showinfo("","Error! Only letters a-z allowed!")
    else:
        homePage()

# đăng kí tài khoảng
def create_Account():
    account_send = []

    username = sign_up_usn.get()
    password = sign_up_psw.get()
    confirm_password = pws_confirm.get()

    if(username == "" or password == "" ):
        messagebox.showinfo("", "Blank not allowed")
    elif (len(username) >= 30) or (len(password) >= 30):
        messagebox.showinfo("","Too much character" + "\n" + "The username or password must less than 30 character")
    elif not (re.match("^[a-zA-Z0-9]*$",username) and re.match("^[a-zA-Z0-9]*$",password)):
         messagebox.showinfo("","Error! Only letters a-z allowed!")
    else:
        if confirm_password == password:
            account_send.append(sign_up_usn)
            account_send.append(sign_up_psw)
            homePage()            
        else:
            messagebox.showinfo("","Incorrect password !")
            
# trang để đăng kí
def registerPage():
    hide_frame()

    global sign_up_psw
    global sign_up_usn
    global pws_confirm

    sign_up_psw = StringVar()
    sign_up_usn = StringVar()
    pws_confirm = StringVar()

    label_page = tk.Label(frame3,text="SIGN UP", font=("Georgia", 20),foreground='blue')

    label_username = tk.Label(frame3, text="Username", height=2)
    sign_up_usn = tk.Entry(frame3, width=30)

    label_password = tk.Label(frame3, text="Password", height=2)
    sign_up_psw = tk.Entry(frame3, width=30)

    label_confirm = tk.Label(frame3, text= "Confirm", height=2)
    pws_confirm = tk.Entry(frame3,width=30)
    
    button_login = tk.Button(frame3,text="Login", width=10, bg='cyan', command=create_Account)
    back_button = tk.Button(frame3, text='Back', width=10,command=lambda:startPage())
    back_button.place(x = 600, y = 10)

    frame3.pack(fill="both", expand=1)
    
    label_page.place(x=300, y=15)
    label_username.place(x=200, y=50)
    sign_up_usn.place(x=270, y=58)
    label_password.place(x=200, y=90)
    sign_up_psw.place(x=270, y=98)
    label_confirm.place(x = 200, y = 130)
    pws_confirm.place(x= 270,y=138)
    button_login.place(x=300, y=168)

# ẩn frame cũ khi chuyển frame
def hide_frame():
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()

# đây là trang đăng nhập
def startPage():
   hide_frame()
   global entry_username
   global entry_password

   entry_password = StringVar()
   entry_username = StringVar()
   
   app_name = tk.Label(frame1, text="nCovi",
                    font=("Georgia", 20), foreground='blue')
   label_username = tk.Label(frame1, text="Username", height=2)
   entry_username = tk.Entry(frame1, width=30)
   label_password = tk.Label(frame1, text="Password", height=2)
   entry_password = tk.Entry(frame1, width=30)
   button_login = tk.Button(frame1,text="Login", width=10, bg='cyan', command=check_login)
   button_register = tk.Button(frame1,text="Register", width=10, bg='cyan', command=registerPage)

   frame1.pack(fill="both", expand=1)
   
   
   app_name.place(x = 300)
   

   label_username.place(x= 190, y= 50)
   entry_username.place(x= 260, y = 60)
   label_password.place(x=190, y =90)
   entry_password.place(x= 260, y = 100)
   entry_password.config(show='*')
   button_login.place(x= 240, y = 130)
   button_register.place(x= 350, y = 130)

# Thoát chương trình
def close_App():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

# trang chính
def homePage():
    hide_frame()
    frame2.pack(fill="both", expand=1)
    page_name = tk.Label(frame2, text="SERVER", font=("Georgia",20), foreground="blue")
    page_name.place(x=245)
    
    logout_button = tk.Button(frame2, text='Logout', width=10,command=lambda:startPage())
    logout_button.place(x = 600, y = 10)
    quit_button = tk.Button(frame2, text='Quit',width=10, command=close_App)
    quit_button.place(x=600,y = 45)

    user_info = tk.Label(frame2, text=("Server: " + str(HOST) + "  -  " + str(SERVER_PORT)))
    user_info.place(x=220, y=55)

    txt = tk.Text(frame2, width=60, height=20, wrap="word")
    txt.place(x=100, y=80)

#startPage()
homePage()
#registerPage()

window.mainloop()