from tkinter import ttk
import tkinter as tk
import db_con




def open_gui(root,newfile):

    # root.geometry('1920x1080')

    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))




    def onFrameConfigure(canvas):
        # Reset the scroll region to encompass the inner frame
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas = tk.Canvas(root, borderwidth=0, selectborderwidth=0, highlightthickness=0)
    frame = tk.Frame(canvas, borderwidth=0, highlightthickness=0)
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    hsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)

    canvas.configure(yscrollcommand=vsb.set)
    canvas.configure(xscrollcommand=hsb.set)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4, 4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))







    # Dictionary with options
    choices = ['Choose a Client', 'Client 1', 'Client 2', 'Client 3', 'Client 4', 'Client 5']

    v = []
    k = tk.StringVar(root)
    choiceso = []
    place = [[]]

    text = [[] for i in range(3)]
    text1 = [[] for i in range(3)]
    purpose = []
    remarks = []
    cli = []
    m = 0
    n = 0
    entries = 0
    extra_field = ["Client", "Purpose", "Remarks"]
    s = ttk.Style()

    # b=tk.OptionMenu(frame, k, *choiceso)

    # print(b.winfo_class())
    print(s.layout('TMenubutton'))
    r = 0
    c = 0
    f = open(newfile, "r")
    flag = True
    count = 0
    s1 = f.readline()

    def get_client_list():
        choiceso.clear()
        choiceso.append("Choose a Client")
        ret = []
        ret = db_con.get_client_db_list()
        for i in ret:
            choiceso.append(i)

    get_client_list()
    print(choiceso)

    while flag:
        s2 = f.readline()
        for i in s2:
            if i == '|':
                flag = False
        if s2 == "\n":
            continue
        '''v.set(s1)
        print(v.get())
        entry.append(tk.Entry(textvariable=v, state="readonly", bd=0, width=100))
        entry[entries].grid(row=r)'''
        tk.Label(frame, text=s1).grid(row=r, columnspan="20", sticky="W", ipadx=5)
        entries += 1
        r += 1
        print(s1)
        s1 = s2

    print(choices)
    while True:

        l = s1.split('|')

        last = l.pop()
        str1 = ""
        for i in last:
            if i != '\n':
                str1 = str1 + i
        l.append(str1)
        c = 0

        print(r)
        if flag == False:
            for i in l:
                tk.Label(frame, text=i, wraplength=200, justify="left").grid(row=r, column=c, sticky="WE", ipadx=5,
                                                                             ipady=10)
                c += 1

            for i in extra_field:
                tk.Label(frame, text=i).grid(row=r, column=c, ipadx=5, ipady=10, columnspan=1)
                c += 1
            flag = True
        elif s1 != "\n":

            for i in l:
                if i == "CR":
                    tk.Label(frame, text="+", wraplength=200, justify="left", fg="green", font="20").grid(row=r,
                                                                                                          column=c,
                                                                                                          sticky="WE",
                                                                                                          ipadx=5,
                                                                                                          ipady=10)
                    c += 1
                elif i == "DR":
                    tk.Label(frame, text="-", wraplength=200, justify="left", fg="red", font="20").grid(row=r, column=c,
                                                                                                        sticky="WE",
                                                                                                        ipadx=5,
                                                                                                        ipady=10)
                    c += 1
                else:
                    tk.Label(frame, text=i, wraplength=200, justify="left").grid(row=r, column=c, sticky="WE", ipadx=5,
                                                                                 ipady=10)
                    c += 1

            for i in range(3):
                print("line:135")
                print(m)
                if i == 0:
                    v.append(tk.StringVar(root))
                    v[m].set('fu')
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
                    '''if i==1:
                        print(text[i][0].get('1.0',tk.END))
                        purpose.append(text[i][0].get('1.0',tk.END))
                    elif i==3:
                        remarks.append(text[i][1].get('1.0',tk.END))'''
                    # print(c)
            m += 1

        s1 = f.readline()
        r += 1
        if not s1:
            break

    print("line:166")
    print(m)
    print("line:168")
    print(text[0])

    def prepare_list():
        a = 0
        check = ""
        for i in range(3):
            for j in range(len(text[0])):
                if i == 0:
                    check = str(v[a].get())
                    if check == "Choose a Client":
                        cli.append("")
                    else:
                        cli.append(str(v[a].get()))
                    a += 1
                elif i == 1:
                    purpose.append(text[i][j].get('1.0', tk.END))
                elif i == 2:
                    remarks.append(text[i][j].get('1.0', tk.END))
        prep = [[] for k in range(2)]
        prep1 = []
        print(purpose)
        print("libe:152")
        print(remarks)
        for i in range(len(text[0])):
            prep1.append(cli[i])
            prep1.append(purpose[i])
            prep1.append(remarks[i])
        print(prep1)
        '''prep1=purpose
        prep[0].append(purpose)
        prep[1].append(remarks)
        prep1.append(remarks)
        print(prep)
        print(prep[1][2])'''
        db_con.add_to_db(prep1)

    def refresh_list():
        n = 0
        print("line:198")
        print(text[0])
        text[0].clear()
        for i in range(m):
            print(i)
            check = v[i].get()
            print("line:194")
            print(v[i].get())
            print("line:196")
            '''for k in range(len(v)):
                print(v[k].get())
            print("line:198")
            print(check)
            if str(check)=="Choose a client":
                 choiceso[0]="Choose a client"
            else:
                 choiceso[0]=check'''
            choiceso[0] = v[i].get()
            print(len(place) - 1)
            print(choiceso)
            # text[0].clear()
            text[0].append(ttk.OptionMenu(frame, v[i], *choiceso))
            print("line 217")
            print(text[0])
            print(i)
            text[0][i].config(width=20)
            text[0][i].grid(row=int(place[i + 1][0]), column=int(place[i + 1][1]), padx=10, pady=10, sticky="E")
            for k in range(len(v)):
                print(v[k].get())
            n += 1

    print(place)
    print(text[0])

    def client_list():
        # choices.append(add_client.get('1.0',tk.END))
        db_con.add_client(add_client.get('1.0', tk.END))
        get_client_list()
        refresh_list()
        # for i in

    add_client = tk.Text(frame, width=20, height=2, highlightthickness=0)
    c = c / 2
    d = int(c)
    add_client.grid(row=3, column=9, padx=10, pady=10,columnspan=2)
    add_client_button = tk.Button(frame, text="Add Client", command=client_list,padx="15")
    r += 5
    add_client_button.grid(row=3, column=9,sticky="W")
    b1 = tk.Button(frame, text="Add Records To Database", command=prepare_list)
    # c=c/2
    b1.grid(row=r + 1, column=d)
    print(text[0][1])
    '''for i in range(m-1):
        print(v[i].get())'''
    # print(text[i][0].get())
    # print(text[i][1])
    

    root.mainloop()

