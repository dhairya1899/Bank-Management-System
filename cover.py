import tkinter as tk
from fileinput import filename
from tkinter import Entry
from tkinter import filedialog as fd
import gui

root = tk.Tk()

root.geometry('400x400')

frame = tk.Frame(root, borderwidth=0, highlightthickness=0)
frame.pack()


newfile = ""
def browsefunc():
    global filename
    global newfile
    filename = fd.askopenfilename()
    for i in filename:
        if (i == '/'):
            newfile += '\\\\'
        else:
            newfile += i
    e.delete(0, tk.END)
    e.insert(0, newfile)


def del_frame():
    frame.pack_forget()
    frame.destroy()
    gui.open_gui(root, newfile)


button1 = tk.Button(frame, text="Browse", command=browsefunc, bg="#7f7fff", fg="white")
button1.pack()
e = Entry(frame, width=40)
e.pack()
button2 = tk.Button(frame, command=del_frame, text="Open", bg="#7f7fff", fg="white")
button2.pack()
root.mainloop()
