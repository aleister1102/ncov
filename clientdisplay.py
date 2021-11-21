import tkinter as tk
from typing import Sized

# đây là trang đăng nhập
def startPage(window_startpage):
   startpage_frame = tk.Frame(window_startpage)
   
   app_name = tk.Label(startpage_frame, text="nCovi",
                    font=("Georgia", 20), foreground='blue')
   label_username = tk.Label(startpage_frame, text="username", height=2)
   entry_username = tk.Entry(startpage_frame, width=30)
   label_password = tk.Label(startpage_frame, text="password", height=2)
   entry_password = tk.Entry(startpage_frame, width=30)
   button_login = tk.Button(startpage_frame,text="login", width=10, bg='cyan')
   button_register = tk.Button(startpage_frame,text="register", width=10, bg='cyan')

   app_name.place(x=270, y=15)
   label_username.place(x=150, y=50)
   entry_username.place(x=220, y=58)
   label_password.place(x=150, y=90)
   entry_password.place(x=220, y=98)
   button_login.place(x=220, y=138)
   button_register.place(x=320, y=138)

# đây là trang xem thông tin
def homePage(window_homepage):
    homepage_frame = tk.Frame(window_homepage)
    label_title = tk.Label(window_homepage,text='Home Page')

    label_title.pack()


def main():
    window = tk.Tk()
    frame = tk.Frame(window)

    window.title("nCovi_project")
    window.geometry("600x400")
    window.resizable(width=False, height=False)

    startPage(frame)
    
    window.mainloop()

    
   


main()

