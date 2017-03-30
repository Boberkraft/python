

class User:
    """Instance is given to user as a interface
    Server can invoke get_msg and ping"""
    access = {'msg', 'list_users', 'poke'}

    def __init__(self, server, connection, functions):
        assert connection is not None, 'Who are you?'
        print(functions)
        self.server = server  # server
        self.connection = str(connection)  # connection
        self.functions = functions
        self.username = functions['username']  # username


    def exposed_do(self, command, data):
        """Execute on server site"""
        if command in self.access:
            # execute. What if server lags? idk
            getattr(self, 'do_' + command)(*data)


    def get(self, command, data):
        """Execture on client site"""
        if command in self.functions:
            # execute. What if server lags? idk
            # self.functions[command](*data)
            getattr(self, 'get_'+command)(data)

    # ------------------ DEFINED FUNCTIONALITY -----------------------
    # at end you need to invoke self.server.send to send something to another user

    # structure of message
    # self.server.send(where, what, who)
    # :where -> name of destination user
    # :what -> ['command_name', info] where info can vary
    # :who -> who is sending this. Use self.

    def do_msg(self, where, what):
        """Sends message to someone"""

        what = ['msg', {'who': str(self), 'what': str(what)}]
        self.server.send(where, what, self)

    def get_msg(self, msg_data):
        msg_data = tuple(msg_data.items())
        self.functions['msg'](msg_data)

    def do_list_users(self):
        """List every user"""
        # maybe i should return value directly to caller?
        what = ['list_users', str(list(self.server.usernames))]
        self.server.send(str(self), what, self)

    def get_list_users(self, all_users):
        self.functions['list_users'](all_users)

    def do_poke(self, where):
        """Pokes someone"""
        what = ['poke', str(self)]
        self.server.send(where, what, self)

    def get_poke(self, all_users):
        self.functions['poke'](all_users)



    # -------------- END OF DEFINED FUNCTIONALITY -------------------

    def __str__(self):
        """return name of user"""
        return self.username

    def __repr__(self):
        """return connection of user"""
        return self.connection
