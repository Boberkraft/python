import rpyc
from tkinter import *
from exceptions import *
from myuser import MyUser
from server import Server
from validate import Validate


class ChatService(rpyc.SlaveService):

    def exposed_connect(self, functions):
        """Function returning interface for sending messages"""
        connection = self.exposed_getconn()  # identifying connection
        client_functions = Validate.check_client(functions)
        new_user = MyUser(server, connection, client_functions)  # makes new user
        if server.add_user(new_user):
            # user can be added
            print('Connected users:', list(server.usernames.keys()))
            # client.conn = new_user  # oh cant do this
            return new_user
        else:
            return False

    # why do i need override this?
    def on_connect(self):
        pass


    def on_disconnect(self):
        # removing disconnected user
        conn = self.exposed_getconn()
        server.remove_user(conn=conn)


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ChatService, port=18812)
    server = Server()
    t.start()

