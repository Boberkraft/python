import rpyc
from tkinter import *

class UsernameTaken(Exception): pass
class InvalidCommunication(Exception): pass
class UsernameNotFound(Exception): pass
class HackDetected(Exception):pass

class Validate:
    @staticmethod
    def check_client(info):
        data = {}
        try:
            data['username'] = info['username']
            data['get_msg'] = info['get_msg']
            if not not data['username'] or not data['username'].isalnum():
                raise AttributeError
        except AttributeError as ee:
            raise AttributeError("Sorry you don't have :", ee)
        if type(data['username']) != str:  # sorry for type checking :/
            raise AttributeError('Username is not a string')
        return data

class User:
    """Instance is given to user as a interface
    Server can invoke get_msg and ping"""
    def __init__(self, connection=None, username=None, get_msg=None):
        assert connection is not None, 'Who are you?'


        self.server = server  # server
        self.connection = str(connection)  # connection
        self.name = username  # username
        try:
            self.get_msg = get_msg  # function for sending msg
            # self.ping = communication['ping']  # function for pinging
        except KeyError:
            msg = """No communication functions found\n
             send {'get_msg': retrieve, 'ping': ping}"""
            raise InvalidCommunication(msg)

    def exposed_send_msg(self, where, what):
        if self.server.check_user(self):
            raise HackDetected('Are You Really Who You Think You Are?')
        self.server.send_msg(self, where, what)

    def __str__(self):
        """return name of user"""
        return self.name

    def __repr__(self):
        """return connection of user"""
        return self.connection


class Server:
    """Main server having control of adding users and invoking functions on usersite"""
    def __init__(self):
        self.connections = {}  # connection: user object
        self.usernames = {}  # username: user object

    def send_msg(self, who, where, what):
        """invokes 'send_msg' function in chosen user"""
        where = self.get_user(where)
        if where:
            where.get_msg({'who': str(who), 'what': str(what)})

    def get_user(self, name=None, conn=None):
        """Retrieves user object basing on username or connection"""
        if name:
            return self.usernames.get(name, False)
        elif conn:
            return self.connections.get(str(conn), False)
        else:
            return False

    def add_user(self, user):
        """Adds user to server"""
        if not self.get_user(name=str(user)) and user.connection not in self.connections:
            # checks user connection and name
            self.usernames[str(user)] = user
            self.connections[repr(user)] = user
            return True
        else:
            raise UsernameTaken('Username already taken. Choose another')

    def check_user(self, user):
        username = self.get_user(name=user.username)
        connection = self.get_user(conn=user.connection)

        if(username is connection) and username is not False:
            return True
        return False

    def remove_user(self, name=None, conn=None):
        """Remove user basing on connection """
        user = self.get_user(name, conn)  # find user
        if user:
            # delete
            self.show_users()  # show users
            del self.connections[repr(user)]
            del self.usernames[str(user)]

        else:
            print('Someone disconnected without logging in')

    def remove_all_users(self):
        """Removes all users"""
        del self.connections
        del self.usernames

    def show_users(self):
        print('Connected users:', list(server.usernames.keys()))

class ChatService(rpyc.SlaveService):

    def exposed_connect(self, info):
        """Function returning interface for sending messages"""
        connection = self.exposed_getconn()  # identifying connection
        client_data = Validate.check_client(info)
        print(client_data)
        new_user = User(connection, **client_data)  # makes new user
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

