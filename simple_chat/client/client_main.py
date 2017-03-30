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

        Label(self.root, text='To who').pack(fill=X)
        self.input_where = Entry(self.root)
        self.input_where.pack(fill=X)
        Label(self.root, text='Message').pack(fill=X)
        self.input_what = Entry(self.root)
        self.input_what.pack(fill=X)

        Button(self.root, text='Send', command=self.send_msg).pack()

        self.display_data()

    # def refresh(ff):
    #     def helper(self, *args, **kwargs):
    #         res = ff(self, *args, **kwargs)
    #         self.display_data()
    #         return res
    #     return helper

    # @refresh
    def exposed_get_msg(self, msg_data):
        msg_data = dict(msg_data)
        msg = '[{who}]: {what}'.format(**msg_data)
        self.to_read.put(msg)

    # @refresh
    def send_msg(self):
        where = self.input_where.get()
        what = self.input_what.get()
        self.conn.do('msg', [where, what])


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
        info['msg'] = self.exposed_get_msg
        info['private_msg'] = self.exposed_get_msg
        info['ping'] = self.exposed_get_msg
        info['list_users'] = self.exposed_get_msg

        return info

root = Tk()


gui = GUI(root)

gui.exposed_username = input('Your username: ')
# information = {'username': gui.exposed_username,
#                'get_msg': gui.exposed_get_msg}
gui.conn = c.root.connect(gui.get_information())
root.title(gui.exposed_username)
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