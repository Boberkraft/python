from tkinter import *
from tkinter.ttk import *
from exceptions import *
import tkinter.simpledialog
from tkinter import ttk
import rpyc
import queue
from queue import Queue
from queue import Empty




class GUI2:

    port_entry = None
    ip_entry = None
    username_entry = None
    msg_entry = None
    chat_box = None
    online_box = None
    connected_label = None
    conn = None

    exposed_username = None

    def __init__(self, root):
        self.port_entry = StringVar(value=18812)
        self.ip_entry = StringVar(value='localhost')
        self.username_entry = StringVar(value='Bobi')
        self.connected_label = StringVar(value='...')
        self.to_who = StringVar(value='')
        self.msg_entry = StringVar()
        self.chat_box = None
        self.online_box = None

        self.root = root

        master = ttk.Frame(root)
        master.pack(padx=10, pady=10)


        left_panel = Frame(master)
        left_panel.pack(side=LEFT)

        right_panel = Frame(master)
        right_panel.pack(fill=BOTH, side=LEFT)

        Label(right_panel, text='Online').grid()
        self.online_box = Text(right_panel, width=10, height=5)
        self.online_box.grid(padx=5, pady=4)

        Label(right_panel, text="To who:").grid()
        Entry(right_panel, textvariable=self.to_who).grid()

        tabs = ttk.Notebook(left_panel)

        chat_tab = Frame(tabs)
        chat_tab.pack()
        self.chat_box = Text(chat_tab, width=40, height=15)
        self.chat_box.grid()

        sending_box = Frame(chat_tab)

        self.msg_entry = Entry(sending_box)
        self.msg_entry.grid(row=0, column=0, sticky=EW)
        Button(sending_box, text='Send', command=self.send_msg).grid(row=0, column=1, sticky='we')

        sending_box.grid(sticky=NSEW)
        sending_box.grid_columnconfigure(0, weight=1)

        options_tab = Frame(tabs)

        login = Frame(options_tab)
        login.pack(expand=True, pady=30)
        Label(login, text='Ip').grid(row=0, column=0)
        Label(login, text='Port').grid(row=1, column=0)
        Label(login, text='Username').grid(row=3, column=0)
        Separator(login, orient=HORIZONTAL).grid(row=2, column=0, columnspan=2, sticky=EW, pady=5)
        Entry(login, textvariable=self.ip_entry).grid(row=0, column=1)
        Entry(login, textvariable=self.port_entry).grid(row=1, column=1)
        Entry(login, textvariable=self.username_entry).grid(row=3, column=1)
        Separator(login, orient=HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=EW, pady=5)
        Button(login, text='Connect', command=self.login).grid(row=5, column=0, columnspan=2)
        Label(login, text='Status:').grid(row=6, column=0, pady=30)

        Label(login, textvariable=self.connected_label).grid(row=6, column=1)

        tabs.add(chat_tab, text='Chat')
        tabs.add(options_tab, text='Options')

        tabs.pack(fill=BOTH, expand=Y)

    def login(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        self.exposed_username = self.username_entry.get()
        print('Adress', ip,':', port)

        self.c = rpyc.connect(str(ip), str(port))
        try:
            self.conn = self.c.root.connect(self.information)
        except Exception as ee:
            print(ee)  # sorry
            self.connected_label.set('Failed!')
        else:
            self.connected_label.set('Connected!')
        self.bgsrv = rpyc.BgServingThread(self.c)
        self.do_list_users()

    def add_to_chat(self, text):
        self.chat_box.insert(END, '%s\n' % text)

    # -------------------------- INTERACTION WITH SERVER --------------------------

    def send_msg(self):
        text = self.msg_entry.get()
        where = self.to_who.get()
        self.conn.do('msg', [where, text])

    def exposed_get_msg(self, msg_data):
        msg_data = dict(msg_data)
        text = '[{who}]: {what}'.format(**msg_data)
        self.add_to_chat(text)

    def do_list_users(self):
        self.conn.do('list_users')
        self.root.after(3000, self.do_list_users)

    def exposed_get_list_users(self, users):
        text = ''
        for user in users:
            text += user + '\n'
        self.online_box.delete(1.0, END)
        self.online_box.insert(END, text)

    # -----------------------END OF INTERACTION WITH SERVER --------------------------

    @property
    def information(self):
        info = {}
        info['username'] = self.exposed_username
        info['msg'] = self.exposed_get_msg
        info['private_msg'] = self.exposed_get_msg
        info['ping'] = self.exposed_get_msg
        info['list_users'] = self.exposed_get_list_users

        return info
root = Tk()

gui = GUI2(root)


root.title(gui.exposed_username)
gui.root.mainloop()



gui.bgsrv.stop()
gui.c.close()