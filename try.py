from tkinter import ttk
import tkinter as tk
import db_con
from tkinter import messagebox
import itertools
from fileinput import filename
from tkinter import Entry
from tkcalendar import Calendar, DateEntry

from tkinter import filedialog as fd


class db_obj():
    host = ""
    user = ""
    password = ""
    db_name = ""

    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name


def add_records():
    separate_lines(f, True)


def display_file():
    global f
    separate_lines(f, False)


def validate_file(new_file):
    global f, file_open
    temp = new_file.split('.')
    temp1 = temp.pop()
    if temp1 == "":
        pass
    elif temp1 != "psv":
        messagebox.showwarning("Warning", "Please Select a psv file")
        return False
    else:
        f = open_file(new_file)
        file_open = True
        var = False
        lines = 0
        while True:
            s2 = f.readline()
            if not s2:
                break
            if s2 == "\n":
                continue
            if "|" not in s2:
                continue
            else:
                l = s2.split('|')
                if lines == 0:
                    no_of_feilds = len(l)
                    lines += 1
                else:
                    if no_of_feilds == len(l):
                        lines += 1
                        var = True
                        continue
                    else:
                        var = False
                        messagebox.showwarning("Warning", "Not a valid file")
                        break
        return var


def create_data_base(db_object):
    global db_open
    db_open = db_con.open_db(db_object)
    if db_open:
        messagebox.showerror("Error", "Please Enter Valid Fields")
    elif not db_open:
        messagebox.showinfo("Success", "Connection Successfull")
        del db_object
        data_base_setting_frame.destroy()
        ti.destroy()
        get_client_list()


def data_base_check():
    global ti
    ti = tk.Toplevel(root)
    ti.geometry('300x250')
    ti.grab_set()
    global data_base_setting_frame
    data_base_setting_frame = tk.Frame(ti, borderwidth=0, highlightthickness=0)
    data_base_setting_frame.pack()
    data_base_setting_frame_hostname = tk.Label(data_base_setting_frame, text="URL (HOST)")
    data_base_setting_frame_hostname.pack()
    data_base_setting_frame_host = tk.Entry(data_base_setting_frame, width=40)
    data_base_setting_frame_host.pack()
    data_base_setting_frame_username = tk.Label(data_base_setting_frame, text="USERNAME")
    data_base_setting_frame_username.pack()
    data_base_setting_frame_user = tk.Entry(data_base_setting_frame, width=40)
    data_base_setting_frame_user.pack()
    data_base_setting_frame_pass = tk.Label(data_base_setting_frame, text="PASSWORD")
    data_base_setting_frame_pass.pack()
    data_base_setting_frame_password = tk.Entry(data_base_setting_frame, show="*", width=40)
    data_base_setting_frame_password.pack()
    data_base_setting_frame_db = tk.Label(data_base_setting_frame, text="DATABASE NAME")
    data_base_setting_frame_db.pack()
    data_base_setting_frame_database_name = tk.Entry(data_base_setting_frame, width=40)
    data_base_setting_frame_database_name.pack()
    data_base_setting_frame_button = tk.Button(data_base_setting_frame, text="Connect Database",
                                               command=lambda: create_data_base(
                                                   db_obj(data_base_setting_frame_host.get(),
                                                          data_base_setting_frame_user.get(),
                                                          data_base_setting_frame_password.get(),
                                                          data_base_setting_frame_database_name.get())))
    data_base_setting_frame_button.pack()


def browse_func():
    new_file = ""
    file_name = fd.askopenfilename()
    for i in file_name:
        if i == '/':
            new_file += '\\\\'
        else:
            new_file += i
    flag = validate_file(new_file)
    if flag:
        embed_frame()
        display_file()


def display_menu():
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=lambda: browse_func())
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=lambda: on_closing())
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Add Client", command=lambda: add_client_mainmenu())
    menubar.add_cascade(label="Remove Client", command=lambda: remove_client_mainmenu())
    menubar.add_cascade(label="Database Settings", command=lambda: data_base_check())
    # menubar.add_cascade(label="Search", command=lambda: Retrieve_from_database())
    search_menu = tk.Menu(menubar, tearoff=0)
    search_menu.add_command(label="Search by Client Name", command=lambda: search_name())
    search_menu.add_command(label="Search by Date", command=lambda: search_date())
    search_menu.add_command(label="Search by Amount", command=lambda: search_by_amt())
    search_menu.add_command(label="Search by Credit/Debit", command=lambda: search_credit())
    menubar.add_cascade(label="Search", menu=search_menu)
    root.config(menu=menubar)


def open_file(path):
    return open(path, "r")


def set_root_geo(root):
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))
    root.state('zoomed')


def onFrameConfigure(canvas):
    # Reset the scroll region to encompass the inner frame
    canvas.configure(scrollregion=canvas.bbox("all"))


def scrollbar(canvas):
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    hsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=vsb.set)
    canvas.configure(xscrollcommand=hsb.set)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))


def embed_frame():
    global canvas
    try:
        canvas.destroy()
        list = root.pack_slaves()
        for l in list:
            l.destroy()
        canvas = tk.Canvas(root, borderwidth=0, selectborderwidth=0, highlightthickness=0)
    except NameError:
        canvas = tk.Canvas(root, borderwidth=0, selectborderwidth=0, highlightthickness=0)
    global frame
    try:
        frame.destroy()
        frame = tk.Frame(canvas, borderwidth=0, highlightthickness=0)
    except NameError:
        frame = tk.Frame(canvas, borderwidth=0, highlightthickness=0)
    scrollbar(canvas)


def print_text(r, s1):
    tk.Label(frame, text=s1).grid(row=r, columnspan="20", sticky="W", ipadx=5)


def show_text_box(r, c):
    global v, text, lis
    for i in range(3):
        if i == 0:
            v.append(tk.StringVar(root))
            m = len(v) - 1
            text[i].append(ttk.OptionMenu(frame, v[m], *choiceso))
            text[i][m].config(width=20)
            lis = []
            lis.append(str(r))
            lis.append(str(c))
            place.append(lis)
            text[i][m].grid(row=r, column=c, padx=10, pady=10, sticky="E")
            c += 1
        else:

            text[i].append(tk.Text(frame, width=25, height=4, highlightthickness=0))
            text[i][m].grid(row=r, column=c, padx=10, pady=10)
            c += 1


def get_client_list():
    choiceso.clear()
    choiceso.append("Choose a Client")
    ret = db_con.get_client_db_list()
    for i in ret:
        choiceso.append(i)
    return ret


def refresh_list():
    ret = get_client_list()
    choiceso.remove("Choose a Client")
    for i in range(len(v)):
        temp = v[i].get()
        text[0][i]['menu'].delete(0, 'end')
        for choice in choiceso:
            text[0][i]['menu'].add_command(label=choice, command=tk._setit(v[i], choice))
        v[i].set(temp)


def add_client_to_db(add_client_mainmenu_text, error):
    client_name = add_client_mainmenu_text.get()
    data = db_con.add_client(client_name)
    error.labelText = data
    error.config(text=data)
    refresh_list()


def remove_client_to_db(checkvalue, r, remove_client_mainmenu_frame):
    for i in range(len(checkvalue)):
        if checkvalue[i].get():
            db_con.change_client_flag(choiceso[i])
    refresh_list()
    update_remove(r, remove_client_mainmenu_frame)


def print_table(l, r, flag):
    get_client_list()

    extra_field = ["Client", "Purpose", "Remarks"]
    c = 0
    if not flag[0]:
        for i in l:
            tk.Label(frame, text=i, wraplength=200, justify="left").grid(row=r, column=c, sticky="WE", ipadx=5,
                                                                         ipady=10)
            c += 1

        for i in extra_field:
            tk.Label(frame, text=i).grid(row=r, column=c, ipadx=5, ipady=10, columnspan=1)
            c += 1
        flag[0] = True

    else:
        for i in l:
            if i == "CR":
                tk.Label(frame, text="+", wraplength=200, justify="left", fg="green", font="20").grid(row=r, column=c,
                                                                                                      sticky="WE",
                                                                                                      ipadx=5, ipady=10)
                c += 1
            elif i == "DR":
                tk.Label(frame, text="-", wraplength=200, justify="left", fg="red", font="20").grid(row=r, column=c,
                                                                                                    sticky="WE",
                                                                                                    ipadx=5, ipady=10)
                c += 1
            else:
                tk.Label(frame, text=i, wraplength=200, justify="left").grid(row=r, column=c, sticky="WE", ipadx=5,
                                                                             ipady=10)
                c += 1
        show_text_box(r, c)


def separate_lines(f, add):
    f.seek(0)
    flag = [False]
    r = 0
    while True:
        final_check = 1
        s2 = f.readline()
        if not s2:
            break
        if s2 == "\n":
            continue
        if "|" not in s2:
            acc_id = s2.split(":")
            if acc_id[0] == "Account Id ":
                t1 = acc_id[1]
                t2 = ""
                for i in range(len(t1)):
                    if t1[i] != " ":
                        t2 = t2 + t1[i]
            if not add:
                print_text(r, s2)
                r += 1
            else:
                continue
        else:
            l = s2.split('|')
            last = l.pop()
            str1 = ""
            for i in last:
                if i != '\n':
                    str1 = str1 + i
            l.append(str1)

            if not add:
                print_table(l, r, flag)
                r += 1
            else:
                if l[0] == "No.":
                    continue
                else:
                    l.append(str(v[r].get()))
                    l.append(text[1][r].get('1.0', tk.END))
                    l.append(text[2][r].get('1.0', tk.END))
                    r += 1
                    check = db_con.add_to_db(l, t2)
                    if not check:
                        final_check = 0
                        messagebox.showerror("Error", "Adding to Database Failed!Try Again")
                        break
    if not add:
        b1 = tk.Button(frame, text="Add Records To Database", command=(lambda: add_records()))
        b1.grid(column=5, columnspan=3)
    if final_check and add:
        messagebox.showinfo("Success", "Records Added Succesfully")


def add_client_mainmenu():
    if db_open:
        messagebox.showerror("Error", "Create a Database Function First")
        data_base_check()
    else:
        global root
        t = tk.Toplevel(root)
        t.geometry('300x250')
        t.grab_set()
        add_client_mainmenu_frame = tk.Frame(t, borderwidth=0, highlightthickness=0)
        add_client_mainmenu_frame.pack()
        add_client_mainmenu_text = tk.Entry(add_client_mainmenu_frame, width=40)
        error = tk.Label(add_client_mainmenu_frame, text='')
        add_client_mainmenu_text.grid(row="5", pady="30", ipady="20")
        add_client_mainmenu_button = tk.Button(add_client_mainmenu_frame, text="Add Client",
                                               command=(lambda: add_client_to_db(add_client_mainmenu_text, error)),
                                               bg="#7f7fff", fg="white")
        add_client_mainmenu_button.grid(row="7")
        error.grid()


def remove_client_mainmenu():
    if db_open:
        messagebox.showerror("Error", "Create a Database Function First")
        data_base_check()
    else:
        global root
        r = tk.Toplevel(root)
        r.geometry('500x500')
        r.grab_set()
        remove_client_mainmenu_frame = tk.Frame(r, borderwidth=0, highlightthickness=20)
        remove_client_mainmenu_frame.pack()
        update_remove(r, remove_client_mainmenu_frame)


def update_remove(r, remove_client_mainmenu_frame):
    remove_client_mainmenu_frame.destroy()
    checkvalue = []
    remove_client_mainmenu_frame = tk.Frame(r, borderwidth=0, highlightthickness=20)
    remove_client_mainmenu_frame.pack()
    for i in range(len(choiceso)):
        checkvalue.append(tk.BooleanVar())
        checkvalue[i].set(False)
        if choiceso[i] != "Choose a Client":
            tk.Checkbutton(remove_client_mainmenu_frame, text=choiceso[i], variable=checkvalue[i]).pack()
    remove_client_mainmenu_button = tk.Button(remove_client_mainmenu_frame, text="Remove Client", command=(
        lambda: remove_client_to_db(checkvalue, r, remove_client_mainmenu_frame)),
                                              bg="#7f7fff", fg="white")
    remove_client_mainmenu_button.pack()


def on_closing():
    global f, file_open, db_open
    if file_open:
        f.close()
    if db_open == 0:
        db_con.close_db()
    root.destroy()


def open_new_search_window():
    global root
    global t
    global data_retrieve_frame
    t = tk.Toplevel(root)
    t.geometry('1000x800')
    t.grab_set()


    data_retrieve_frame = tk.Frame(t, borderwidth=0, highlightthickness=0)
    data_retrieve_frame.pack()


# SEARCH BY NAME
def display_search_name(records, data_retrieve_frame):
    data_retrieve_frame.destroy()
    display_search_name_frame = tk.Frame(t)
    display_search_name_frame.pack()
    r = 0
    c = 0
    # list = [[]]
    for record in records:

        list_of_name = list(record)
        for l in list_of_name:
            tk.Label(display_search_name_frame, text=l, wraplength=200, justify="left").grid(row=r, column=c,
                                                                                             sticky="WE", ipadx=5,
                                                                                             ipady=10)
            c += 1
        c = 0
        r += 1


def call_name_db(name, data_retrieve_frame):
    records = db_con.fetch_from_db(name)
    if len(records) == 0:
        messagebox.showerror("Error", "No such Client found")
    else:
        display_search_name(records, data_retrieve_frame)


def search_name():
    if db_open:
        messagebox.showerror("Error", "Create a Database Function First")
        data_base_check()
    else:
        open_new_search_window()
        all_clients = db_con.get_all_clients()
        all_clients.insert(0, "Choose a client")
        tk.Label(data_retrieve_frame, text="Search By name").grid(row="10")
        client_name = tk.StringVar()
        client_option = ttk.OptionMenu(data_retrieve_frame, client_name, *all_clients)
        client_option.grid()
        add_client_mainmenu_button = tk.Button(data_retrieve_frame, text="Search Client",
                                               command=(lambda: call_name_db(client_name.get(), data_retrieve_frame)),
                                               bg="#7f7fff", fg="white")

        add_client_mainmenu_button.grid(row="12")


# SEARCH BY CREDIT/DEBIT
def search_credit():
    if db_open:
        messagebox.showerror("Error", "Create a Database Function First")
        data_base_check()
    else:
        open_new_search_window()
        OptionList = [
            "Choose A Type",
            "CR",
            "DR"
        ]
        variable = tk.StringVar(data_retrieve_frame)

        opt = ttk.OptionMenu(data_retrieve_frame, variable, *OptionList)
        opt.pack()

        button = tk.Button(data_retrieve_frame, text="Search", bg="#7f7fff", fg="white",
                           command=(lambda: call_credit_from_db(variable.get(), data_retrieve_frame)))
        button.pack()


def call_credit_from_db(name, data_retrieve_frame):
    records = db_con.fetch_from_db_credit(name)
    if len(records) == 0:
        messagebox.showerror("Error", "No such Client found")
    else:
        display_search_name(records, data_retrieve_frame)


def search_date():
    if db_open:
        messagebox.showerror("Error", "Create a Database Function First")
        data_base_check()
    else:
        open_new_search_window()
        calender(data_retrieve_frame)


def calender(data_retrieve_frame):
    def print_sel():
        '''print(cal.selection_get())'''
        tk.Label(data_retrieve_frame, text="Start Date").pack()
        date = ttk.Label(data_retrieve_frame, text=cal.selection_get())
        date.pack()

    cal = Calendar(data_retrieve_frame, font="Arial 14", selectmode='day', locale='en_US',
                   cursor="hand1", year=2018, month=2, day=5)

    cal.pack(fill="both", expand=True)
    ttk.Button(data_retrieve_frame, text="ok", command=print_sel).pack()

#SEARCH BY AMOUNT
def search_by_amt():
    if db_open:
        messagebox.showerror("Error", "Create a Database Function First")
        data_base_check()
    else:
        open_new_search_window()
        tk.Label(data_retrieve_frame, text="Enter the Amount Range").pack()
        name1 = tk.Entry(data_retrieve_frame)
        name1.pack()
        name2 = tk.Entry(data_retrieve_frame)
        name2.pack()
        button = tk.Button(data_retrieve_frame, text="Search", bg="#7f7fff", fg="white",
                           command=(lambda: call_amt_from_db(name1,name2, data_retrieve_frame)))
        button.pack()


def call_amt_from_db(name1,name2, data_retrieve_frame):
    records = db_con.fetch_from_db_amt(name1,name2)
    if len(records) == 0:
        messagebox.showerror("Error", "No such Client found")
    else:
        display_search_name(records, data_retrieve_frame)


root = tk.Tk()
file_open = False

v = []
choiceso = []
db_open = 1
data_base_check()

place = [[]]
text = [[] for i in range(3)]
text1 = [[] for i in range(3)]
purpose = []
remarks = []
cli = []
lis = []
set_root_geo(root)
global f
display_menu()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
