import tkinter as tk
import requests

def open_new(root):
 Label1= tk.Label(root,text="fdnkjfsbdjkfbL",font="30")
 Label1.pack()
 e1 = tk.Entry(root)
 e1.pack()
 print("line:=")


 def urlreq():
     #url = 'https://www.python.org/static/img/python-logo@2x.png'
     url=e1.get()
     myfile = requests.get(url)
     open('/test1.png', 'wb').write(myfile.content)


 button1= tk.Button(root,text="Click",command=urlreq)
 button1.pack()




 root.mainloop()