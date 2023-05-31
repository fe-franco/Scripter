from email.policy import default
from pickle import FALSE
from re import A
from site import USER_BASE
from time import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk, BooleanVar, END
import os
import configparser


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Scripter")
        self.iconbitmap("logo.ico")
        self.option_add("*tearOff", False)
        self.resizable(False, False)
        style = ttk.Style(self)
        # Import the tcl file
        self.tk.call("source", "proxttk-dark.tcl")
        # Set the theme with the theme_use method
        style.theme_use("proxttk-dark")

        self.title_font = tkfont.Font(family='colortube', size=20)
        self.sub_font = tkfont.Font(family='colortube', size=12)
        self.button_font = tkfont.Font(family='colortube', weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

[1,2,3]
{1:2,3:4}

class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        pad = 79
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        titulo = ttk.Label(self, text="Scripter")
        titulo.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=pad)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
