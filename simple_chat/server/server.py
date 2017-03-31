

class Server:
    """Main server having control of adding users and invoking functions on usersite"""
    def __init__(self):
        self.connections = {}  # connection: user object
        self.usernames = {}  # username: user object

    def send(self, where, what, who=None):
        """invokes 'msg' function in chosen user"""
        assert who is not None, 'Who are you?'
        if who is not self and not self.check_user(who):
            raise HackDetected('Are You Really Who You Think You Are?')
        found_user = self.get_user(where)
        if found_user:
            # send what needs to be send
            found_user.get(*what)
        else:
            # send message to himself
            who.get('msg', dict(who='server', what='Count find user'))


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
            user.get('msg', {'who': 'server', 'what': 'Welcome {} on our server!'.format(user)})
            return True
        else:
            raise UsernameTaken('Username already taken. Choose another')

    def check_user(self, user):
        """Check if user can be trusted.
        Return yes if it can"""
        username_username = self.get_user(name=user.username)
        connection_username = self.get_user(conn=user.connection)

        if(username_username is connection_username) and username_username is not False:
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
        print('Connected users:', list(self.usernames.keys()))
