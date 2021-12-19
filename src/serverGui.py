import tkinter as tk
from tkinter import  StringVar, messagebox
from tkinter import ttk
import re
from tkinter.constants import END
import server as se


#Đóng gói hàm lại, không gọi hàm ở ngoài như thế này
window = tk.Tk()

window.title("nCovi_server")
#window.iconbitmap(r'C:\Users\rongc\OneDrive - VNU-HCMUS\Desktop\Study\Code\MMT\ncov-20CTT3\imgs\logo.ico')
window.geometry("720x480")
window.resizable(width=False, height=False)

frame2 = tk.Frame(window)


# Thoát chương trình
def close_App(server):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        se.closeServer(server)
        window.destroy()

# trang chính
def homePage():

    sThread = se.threading.Thread(target=se.openServer)
    sThread.daemon = True 
    sThread.start() 

    frame2.pack(fill="both", expand=1)
    page_name = tk.Label(frame2, text="SERVER", font=("Georgia",20), foreground="blue")
    page_name.place(x=245)
    

    quit_button = tk.Button(frame2, text='Quit',width=10, command=lambda:close_App(se.s))
    quit_button.place(x=600,y = 10)
    
    def seeConnection():
        txt.delete(0, len(se.live_account))
        for i in range(len(se.live_account)):
            txt.insert(i, se.live_account[i])

    
    user_info = tk.Label(frame2, text=("Server: " + str(se.HOST) + "  -  " + str(se.SERVER_PORT)))
    user_info.place(x=220, y=55)
    refresh_button = tk.Button(frame2,text = 'REFRESH', bg='blue',width=15, command=seeConnection)
    refresh_button.place(x = 280, y=430)
    
    global txt
    txt = tk.Listbox(frame2,font=("Arial",15), width=45, height=12)
    scrollbar  = tk.Scrollbar(frame2, orient="vertical", command=txt.yview)
    txt['yscroll'] = scrollbar.set
    scrollbar.place(in_=txt, relx=1.0, relheight=1.0, bordermode="outside")
    txt.place(x=100, y=80)

#se.openServer()
#startPage()
homePage()
#registerPage()

window.mainloop()