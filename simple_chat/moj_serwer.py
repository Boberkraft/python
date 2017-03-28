import rpyc

class UsernameTaken(Exception): pass
class InvalidCommunication(Exception): pass


class User:
    """Server can invoke
    get_msg and ping"""
    def __init__(self, connection=None, name=None, communication=None):
        assert connection is not None, 'Who are you?'
        assert name is not None, 'Whats your name?'
        assert name.isalnum() is True, 'Your name needs to be allphanumerical'

        self.server = server  # server
        self.connection = str(connection)  # connection
        self.name = name  # username
        try:
            self.get_msg = communication['get_msg']  # function for sending msg
            # self.ping = communication['ping']  # function for pinging
        except KeyError:
            msg = """No communication functions found\n
             send {'get_msg': retrieve, 'ping': ping}"""
            raise InvalidCommunication(msg)


    def exposed_send_msg(self, where, what):
        self.server.send_msg(self, where, what)

    def __str__(self):
        """return name of user"""
        return self.name

    def __repr__(self):
        """return connection of user"""
        return self.connection


class Server:

    def __init__(self):
        self.connections = {}  # connection: user object
        self.usernames = {}  # username: user object

    def send_msg(self, who, where, what):
        """invokes 'send_msg' function in chosen user"""
        where = self.get_user(where)
        if where:
            where.get_msg('[{who}]: {what}'.format(who=who, what=what))

    def get_user(self, name=None, conn=None):
        """Retrieves user object basing on username or connection"""
        if name:
            return self.usernames.get(name, False)
        else:
            return self.connections.get([conn], False)

    def add_user(self, user):
        """Adds user to server"""
        if not self.get_user(user) and user.connection not in self.connections:
            # checks user connection and name
            self.usernames[str(user)] = user
            self.connections[repr(user)] = user
            return True
        else:
            raise UsernameTaken('Username already taken. Choose another')

    def remove_user(self, *args, **kwargs):
        """Remove user basing on connection """
        user = self.get_user(*args, **kwargs)  # find user
        if user:
            # delete
            del self.connections[repr(user)]
            del self.usernames[str(user)]
        else:
            print('Someone disconnected without logging in')

    def remove_all_users(self):
        """Removes all users"""
        del self.connections
        del self.usernames


class ChatService(rpyc.SlaveService):

    def exposed_connect(self, *args, **kwargs):
        """Function returning interface for sending messages"""
        connection = self.exposed_getconn()  # identifying connection
        new_user = User(connection, *args, **kwargs)  # makes new user
        if server.add_user(new_user):
            # user can be added - passed tests
            print('Connected users:', list(server.usernames.keys()))
            return new_user  # returning interface
        else:
            return False

    # why do i need override this?
    def on_connect(self):
        pass

    def on_disconnect(self):
        # removing disconnected user
        server.remove_user(conn=self.exposed_getconn())
        print('Connected users:', list(server.usernames.keys()))


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ChatService, port=18812)
    server = Server()
    t.start()

