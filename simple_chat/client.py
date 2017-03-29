from tkinter import *
import rpyc
import queue
from queue import Queue
from queue import Empty

c = rpyc.connect('localhost', 18812)
bgsrv = rpyc.BgServingThread(c)

class GUI:


    def __init__(self, username):
        self.to_read = Queue()
        # self.to_read.put(1122)
        # print(self.to_read.get(block=False))
        self.root = Tk()
        self.conn = None

        self.root.title(username)
        # self.conn = self.exposed_conn
        self.exposed_username = username

        self.box = Text(self.root, width=30, height=10)
        self.box.pack()

        Label(self.root, text='Username').pack(fill=X)
        self.input_where = Entry(self.root)
        self.input_where.pack(fill=X)
        Label(self.root, text='What to send').pack(fill=X)
        self.input_what = Entry(self.root)
        self.input_what.pack(fill=X)

        Button(self.root, text='Wyslij', command=self.xd).pack()

        self.display_data()

    def exposed_get_msg(self, msg):

        # msg = '[{who}]:{what}'.format(msg['who', msg['what']])
        self.to_read.put(msg)

    def send_msg(self):
        where = self.input_where.get()
        what = self.input_what.get()
        self.conn.send_msg(where, what)

    def display_data(self):
        while True:
            try:
                message = self.to_read.get(block=False)
            except Empty:
                break
            else:

                self.box.insert(END, '%s\n' % message)
        self.root.after(100, self.display_data)

    def get_information(self):
        info = {}
        info['username'] = self.exposed_username
        info['get_msg'] = self.exposed_get_msg
        return info

    def xd(self):
        self.conn.server.send_msg(self, '123', 'siemka')
username = input('Username: ')

gui = GUI(username)
# information = {'username': gui.exposed_username,
#                'get_msg': gui.exposed_get_msg}
gui.conn = c.root.connect(gui.get_information())
gui.root.mainloop()
#
# username = input('Your username: ')
#
# # class for interacting with server

#
# while True:
#     where = input('To who: ')
#     what = input('What: ')
#     myself.send_msg(where, what)
#



# root.protocol('WM_DELETE_WINDOW', on_closing)


bgsrv.stop()
c.close()