import tkinter as tk
from tkinter import messagebox
from tkinter.constants import COMMAND

# kiểm tra đăng nhập
def check_login():
    username = entry_username.get()
    password = entry_password.get()

    if(username == "" and password == ""):
        messagebox.showinfo("", "Blank not allowed")
    else:
        homePage()
        


# đây là trang đăng nhập
def startPage(window):

   window.title("nCovi_project")
   window.geometry("600x400")
   window.resizable(width=False, height=False)
   
   global entry_username
   global entry_password
   
   app_name = tk.Label(window, text="nCovi",
                    font=("Georgia", 20), foreground='blue')
   label_username = tk.Label(window, text="username", height=2)
   entry_username = tk.Entry(window, width=30)
   label_password = tk.Label(window, text="password", height=2)
   entry_password = tk.Entry(window, width=30)
   button_login = tk.Button(window,text="login", width=10, bg='cyan', command=check_login)
   button_register = tk.Button(window,text="register", width=10, bg='cyan')

   app_name.place(x=270, y=15)
   label_username.place(x=150, y=50)
   entry_username.place(x=220, y=58)
   label_password.place(x=150, y=90)
   entry_password.place(x=220, y=98)
   entry_password.config(show='*')
   button_login.place(x=220, y=138)
   button_register.place(x=320, y=138)

# đây là trang xem thông tin
def homePage():
    window_homepage = tk.Toplevel(window)
    window_homepage.title("nCovi_project")
    window_homepage.geometry("600x400")
    window_homepage.resizable(width=False, height=False)
 
    label_title = tk.Label(window_homepage,text='Home Page')


    label_title.pack()


def main():
    global window
    window = tk.Tk()
    
    startPage(window)
    
    window.mainloop()

    

main()

