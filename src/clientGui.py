import tkinter as tk
from tkinter import StringVar, messagebox
from tkinter import ttk
from tkinter.constants import ANCHOR, BOTH, CENTER, INSERT, LEFT, RIGHT, TRUE
import requests
import json
import re
import client as cl


global window
window = tk.Tk()

window.title("nCovi_client")
# window.iconbitmap(r'C:\Users\rongc\OneDrive - VNU-HCMUS\Desktop\Study\Code\MMT\ncov-20CTT3\imgs\logo.ico')
window.geometry("600x400")
window.resizable(width=False, height=False)

frame2 = tk.Frame(window, highlightbackground="green", highlightthickness=3)
frame1 = tk.Frame(window, highlightbackground="red", highlightthickness=3)
frame3 = tk.Frame(window, highlightbackground="blue", highlightthickness=3)


# kiểm tra đăng nhập
def check_login(connect):
    account = []

    username = entry_username.get()
    password = entry_password.get()

    account.append(username)
    account.append(password)

    if(username == "" or password == ""):
        messagebox.showinfo("", "Blank not allowed")
    elif (len(username) >= 30) or (len(password) >= 30):
        messagebox.showinfo("", "Too much character" + "\n" +
                            "The username or password must less than 30 character")
    elif not (re.match("^[a-zA-Z0-9]*$", username) and re.match("^[a-zA-Z0-9]*$", password)):
        messagebox.showinfo("", "Error! Only letters a-z allowed!")
    elif cl.sendOption(connect, "1", account) == True:
        homePage(connect)
    else:
        messagebox.showinfo("", "username or password is incorrect")

# đăng kí tài khoảng


def create_Account(connect):
    account_send = []

    username = sign_up_usn.get()
    password = sign_up_psw.get()
    confirm_password = pws_confirm.get()

    if(username == "" or password == ""):
        messagebox.showinfo("", "Blank not allowed")
    elif (len(username) >= 30) or (len(password) >= 30):
        messagebox.showinfo("", "Too much character" + "\n" +
                            "The username or password must less than 30 character")
    elif not (re.match("^[a-zA-Z0-9]*$", username) and re.match("^[a-zA-Z0-9]*$", password)):
        messagebox.showinfo("", "Error! Only letters a-z allowed!")
    else:
        if confirm_password == password:
            account_send.append(username)
            account_send.append(password)
            if cl.sendOption(connect, "0", account_send) == True:
                homePage(connect)
            else:
                messagebox.showinfo("", "The account already exists")
                homePage(connect)
        else:
            messagebox.showinfo("", "Incorrect password !")

# trang để đăng kí


def registerPage(connect):
    hide_frame()

    global sign_up_psw
    global sign_up_usn
    global pws_confirm

    sign_up_psw = StringVar()
    sign_up_usn = StringVar()
    pws_confirm = StringVar()

    label_page = tk.Label(frame3, text="SIGN UP", font=(
        "Georgia", 20), foreground='blue')

    label_username = tk.Label(frame3, text="Username", height=2)
    sign_up_usn = tk.Entry(frame3, width=30)

    label_password = tk.Label(frame3, text="Password", height=2)
    sign_up_psw = tk.Entry(frame3, width=30)

    label_confirm = tk.Label(frame3, text="Confirm", height=2)
    pws_confirm = tk.Entry(frame3, width=30)

    button_login = tk.Button(frame3, text="Login",
                             width=10, bg='cyan', command=lambda: create_Account(connect))

    frame3.pack(fill="both", expand=1)

    label_page.place(x=250, y=15)
    label_username.place(x=150, y=50)
    sign_up_usn.place(x=220, y=58)
    label_password.place(x=150, y=90)
    sign_up_psw.place(x=220, y=98)
    label_confirm.place(x=150, y=130)
    pws_confirm.place(x=220, y=138)
    button_login.place(x=250, y=168)

# ẩn frame cũ khi chuyển frame


def hide_frame():
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()

# đây là trang đăng nhập


def startPage():
    hide_frame()
    connect = cl.connectToServer()
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
    button_login = tk.Button(frame1, text="Login",
                             width=10, bg='cyan', command=lambda: check_login(connect))
    button_register = tk.Button(
        frame1, text="Register", width=10, bg='cyan', command=lambda: registerPage(connect))

    frame1.pack(fill=BOTH, expand=1)

    app_name.place(x=250)

    label_username.place(x=130, y=50)
    entry_username.place(x=200, y=60)
    label_password.place(x=130, y=90)
    entry_password.place(x=200, y=100)
    entry_password.config(show='*')
    button_login.place(x=180, y=130)
    button_register.place(x=290, y=130)

# https://coronavirus-19-api.herokuapp.com/countries
# lấy thông tin covid theo địa điểm


def get_info():
    api_request = requests.get(
        "https://coronavirus-19-api.herokuapp.com/countries")
    api = json.loads(api_request.content)
    api_request_VN = requests.get(
        "https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true&utf8=1")
    api_VN = json.loads(api_request_VN.content)
    location_VN = api_VN['locations']

    info_page.delete(0.0, 'end')
    text_1 = info_entry.get()

    selected = drop.get()

    if selected == "Search by.....":
        info_page.insert(0.0, "You forgot to pick a dropdown menu!")
    elif selected == "World":
        for i in range(len(api)):
            if text_1 == api[i]['country']:
                info_page.insert(0.0, "Country: " + str(api[i]['country']) + "\n" +
                                 "Cases: " + str(api[i]['cases']) + "\n" +
                                 "Deaths: " + str(api[i]['deaths']) + "\n" +
                                 "Recovered: " + str(api[i]['recovered']) + "\n")
    elif selected == "Viet Nam":
        for s in range(len(location_VN)):
            if text_1 == location_VN[s]['name']:
                info_page.insert(0.0, "Province: " + str(location_VN[s]['name'] + "\n")
                                 + "Deaths: " +
                                 str(location_VN[s]['death']) + "\n"
                                 + "Cases: " +
                                 str(location_VN[s]['cases']) + "\n"
                                 + "Recovered: " + str(location_VN[s]['recovered']))

# Thoát chương trình


def close_App(connect):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        cl.closeConnection(connect)


# đây là trang xem thông tin
def homePage(connect):
    hide_frame()

    label_title = tk.Label(frame2, text='Home Page',
                           font=("Georgia", 20), foreground="blue")
    logout_button = tk.Button(frame2, text='Logout',
                              width=10, command=lambda: startPage())

    global info_entry
    global info_page
    global drop
    info_entry = StringVar()

    info_entry = tk.Entry(frame2, width=30)
    info_page = tk.Text(frame2, font=("Arial", 12), width=50, height=15)
    info_page.insert(0.0, "write without accents ")

    ok_button = tk.Button(frame2, text="Ok", width=5,
                          bg="cyan", command=get_info)
    quit_button = tk.Button(frame2, text='Quit', width=10,
                            command=lambda: close_App(connect))
    # combobox
    drop = ttk.Combobox(frame2, values=["Search by.....", "World", "Viet Nam"])
    drop.current(0)

    def click(event):
        info_entry.configure(state="normal")
        info_entry.delete(0, "end")

    frame2.pack(fill=BOTH, expand=1)

    label_title.place(x=10, y=5)
    logout_button.place(x=500, y=10)
    info_page.place(x=100, y=100)
    info_entry.place(x=10, y=50)
    info_entry.insert(0, "enter your location")
    info_entry.configure(state="disabled")
    info_entry.bind("<Button-1>", click)
    ok_button.place(x=350, y=47)
    quit_button.place(x=500, y=45)
    drop.place(x=200, y=50)


startPage()
# homePage()
# registerPage()

window.mainloop()
