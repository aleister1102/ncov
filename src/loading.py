from tkinter import Tk,Label
from time import sleep

class LoadingSplash:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("720x480")
        self.root.resizable(width=False, height=False)
        self.root.config(bg="black")
        self.root.title("Custom loader")
        
        Label(self.root,text = "Loading....",font = "8BIT",
              bg="black",fg="#56c6e8").place(x=200,y=110)
        
        # tạo các block màu đen làm nền
        for i in range(16):
            Label(self.root,bg = "#f3e6fa",width =2,height = 1).place(x=(i+10)*22,y=150)
        
        # cập nhật root
        self.root.update()
        self.play_animation()
        
        # mainloop
        self.root.mainloop()
    
    def play_animation(self):
        for i in range(200):
            for j in range(16):
                # chuyển màu xanh
                Label(self.root,bg="#56c6e8",width =2,height = 1).place(x=(j+10)*22,y = 150)
                sleep(0.06)
                self.root.update_idletasks()
                # chuyển màu tối
                Label(self.root,bg="#f3e6fa",width =2,height = 1).place(x=(j+10)*22,y = 150)
            
        else: 
            self.root.destroy()
            exit()
            
                
    
if __name__ =="__main__":
    LoadingSplash()