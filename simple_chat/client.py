from tkinter import *
import tkinter.simpledialog

import rpyc
import queue
from queue import Queue
from queue import Empty

c = rpyc.connect('localhost', 18812)
bgsrv = rpyc.BgServingThread(c)

class GUI:
    username = None

    def __init__(self, root):
        self.to_read = Queue()
        # self.to_read.put(1122)
        # print(self.to_read.get(block=False))
        self.root = root
        self.conn = None


        # self.conn = self.exposed_conn

        self.box = Text(self.root, width=30, height=10)
        self.box.pack()

        Label(self.root, text='Username').pack(fill=X)
        self.input_where = Entry(self.root)
        self.input_where.pack(fill=X)
        Label(self.root, text='What to send').pack(fill=X)
        self.input_what = Entry(self.root)
        self.input_what.pack(fill=X)

        Button(self.root, text='Wyslij', command=self.send_msg).pack()
        username = tkinter.simpledialog.askstring('Input', 'Enter Username')
        username = tkinter.simpledialog.askstring('Input', 'Enter Username')
        self.display_data()

    def exposed_get_msg(self, msg):
        try:
            # DONT DONT KWARG UNPACING **
            # because dict send by server is not a 100% legit dict :|
            # shoud i send a list o (key, val) tuples?
            print(msg['who'])
            print(msg['what'])
            msg = '[{who}]: {what}'.format(who=msg['who'],what=msg['what'])
        except KeyError:
            print('Server messed dialog')

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

root = Tk()
root.title('Chat')

gui = GUI(root)

gui.exposed_username = 'Bobi'
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