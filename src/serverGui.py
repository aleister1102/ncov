from tkinter import Tk, Frame, Label, Text

window = Tk()
   
window.title("nCovi_server")
window.geometry("600x400")
window.resizable(width=False, height=False)

frame = Frame(window,  highlightbackground="green", highlightthickness=3)

page_name = Label(frame, text="SERVER", font=("Georgia",20), foreground="blue")
page_name.place(x=245)

user_info = Label(frame, text="Login information")
user_info.place(x=240, y=55)

txt = Text(frame, width=50, height=15, wrap="word")
txt.place(x=100, y=80)

frame.pack(fill="both", expand=1)


window.mainloop()