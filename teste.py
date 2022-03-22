import tkinter as tk

app = tk.Tk()

tabelas = []

def resetButton():
    createTabelasButton.grid_remove()
    removeTabelasButton.grid_remove()
    printerButton.grid_remove()
    createTabelasButton.grid(column=0, row=len(tabelas)+1)
    printerButton.grid(column=1, row=len(tabelas)+1)
    removeTabelasButton.grid(column=2, row=len(tabelas)+1)


def createtabelas():

    Tabelas = tk.Entry(app)
    tabelas.append(Tabelas)

    Tabelas.grid(column=0, row=len(tabelas), columnspan=3)
    

    print(len(tabelas))
    resetButton()

def removetabelas():
    createTabelasButton.grid_remove()
    removeTabelasButton.grid_remove()
    tabelas.pop().grid_remove()
    resetButton()
    

createTabelasButton = tk.Button( app, text="+", command=createtabelas)
createTabelasButton.grid(column=0, row=len(tabelas)+1)
removeTabelasButton = tk.Button( app, text="-", command=removetabelas)
removeTabelasButton.grid(column=2, row=len(tabelas)+1)

def printer():
    for i in tabelas:
        print(i.get())

printerButton = tk.Button( app, text="print", command=printer)
printerButton.grid(column=1, row=len(tabelas)+1)

app.mainloop()
