import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

ROOT = tk.Tk()
  # hide naff extra window
ROOT.title('Please choose a date')


def pick_date_dialog():
    '''Display GUI date picker dialog,
       print date selected when OK clicked'''

    def print_sel():
        selected_date = (cal.get_date())

        date1 = tk.Label(frame1, text=selected_date)


    top = tk.Toplevel(ROOT)

    # defaults to today's date
    cal = Calendar(top,
                   font="Arial 10", background='darkblue',
                   foreground='white', selectmode='day')

    cal.grid()
    ttk.Button(top, text="OK", command=print_sel).grid()


pick_date_dialog()

ROOT.mainloop()