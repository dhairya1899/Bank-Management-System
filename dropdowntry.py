import tkinter as tk
from tkinter import ttk

OptionList = [
"Choose",
"Aries",
"Taurus",
"Gemini",
"Cancer"
]

app = tk.Tk()

app.geometry('100x200')

variable = tk.StringVar(app)
variable.set(OptionList[0])

opt = ttk.OptionMenu(app, variable, *OptionList)
opt.pack()
def ok():
    value = tk.Label(app, text = variable.get())
    value.pack()


button = tk.Button(app, text="OK", command=ok)
button.pack()

app.mainloop()