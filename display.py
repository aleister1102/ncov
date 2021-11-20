import tkinter as tk
from typing import Sized

window = tk.Tk()

window.title("nCovi_project")
window.geometry("600x400")
window.resizable(width=False,height=False)

app_name = tk.Label(window, text= "nCovi")
label_username = tk.Label(window, text="username", height= 2)
entry_username = tk.Entry(window, width = 30)
label_password = tk.Label(window, text="password", height=2)
entry_password = tk.Entry(window, width=30)
button_login = tk.Button(text="login", width= 10,bg='cyan')
button_register = tk.Button(text="register",width=10,bg='cyan')

app_name.place(x= 280, y= 15)
label_username.place(x = 150, y=50)
entry_username.place(x = 220, y = 58)
label_password.place(x= 150, y =90 )
entry_password.place(x= 220,y = 98)
button_login.place(x=200, y=138)
button_register.place(x = 300, y=138 )


window.mainloop()