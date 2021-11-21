import tkinter as tk
from tkinter import StringVar, Tk, messagebox


# kiểm tra đăng nhập
def check_login():
    account = []

    username = entry_username.get()
    password = entry_password.get()

    account.append(username)
    account.append(password)

    if(username == "" and password == "" ):
        messagebox.showinfo("", "Blank not allowed")
    else:
        homePage()
        window.destroy()




# trang để đăng kí
def registerPage():
    window.destroy()
    global window_register
    window_register = tk.Tk()

    window_register.title("nCovi_client")
    window_register.geometry("600x400")
    window_register.resizable(width=False, height=False)

    entry_password = StringVar()
    entry_username = StringVar()

    label_page = tk.Label(window_register,text="SIGN UP", font=("Georgia", 20),foreground='blue')

    label_username = tk.Label(window_register, text="Username", height=2)
    entry_username = tk.Entry(window_register, width=30)

    label_password = tk.Label(window_register, text="Password", height=2)
    entry_password = tk.Entry(window_register, width=30)

    #label_confirm = tk.Label(window_register, text= "Confirm", height=2)
    #entry_confirm = tk.Entry(window_register,width=30)
    
    button_login = tk.Button(window_register,text="Login", width=10, bg='cyan', command=check_login)
    
    label_page.place(x=250, y=15)
    label_username.place(x=150, y=50)
    entry_username.place(x=220, y=58)
    label_password.place(x=150, y=90)
    entry_password.place(x=220, y=98)
    #label_confirm.place(x = 150, y = 130)
    #entry_confirm.place(x= 220,y=138)
    button_login.place(x=250, y=168)




# đây là trang đăng nhập
def startPage(window):

   window.title("nCovi_client")
   window.geometry("600x400")
   window.resizable(width=False, height=False)
   
   global entry_username
   global entry_password

   entry_password = StringVar()
   entry_username = StringVar()
   
   app_name = tk.Label(window, text="nCovi",
                    font=("Georgia", 20), foreground='blue')
   label_username = tk.Label(window, text="Username", height=2)
   entry_username = tk.Entry(window, width=30)
   label_password = tk.Label(window, text="Password", height=2)
   entry_password = tk.Entry(window, width=30)
   button_login = tk.Button(window,text="Login", width=10, bg='cyan', command=check_login)
   button_register = tk.Button(window,text="Register", width=10, bg='cyan', command=registerPage)

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
    global window_homepage
    window_homepage = tk.Tk()
    
    window_homepage.title("nCovi_client")
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

