#Import tkinter library
from tkinter import *
from tkinter import ttk, BooleanVar, END
#Create an instance of Tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Make the window sticky for every case
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)
#Create a Label
widgets_frame = ttk.Frame(win, borderwidth=1, relief="solid")
widgets_frame.grid(row=2, column=0)
label=Label(widgets_frame, text="This is a Centered Text",font=('Aerial 15 bold'))
label.grid(row=1, column=0)
label.grid_rowconfigure(1, weight=1)
label.grid_columnconfigure(1, weight=1)
win.mainloop()