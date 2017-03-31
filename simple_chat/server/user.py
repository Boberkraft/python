

class User:
    """Instance is given to user as a interface
    Server can invoke get_msg and ping"""


    def __init__(self, server, connection, functions):
        assert connection is not None, 'Who are you?'
        self.server = server  # server
        self.connection = str(connection)  # connection
        self.functions = functions
        self.username = functions['username']  # username


    def exposed_do(self, command, data=None):
        """Execute on server site"""

        if command in self.access:
            # execute. What if server lags? idk
            if data is not None:
                getattr(self, '_do_' + command)(*data)
            else:
                getattr(self, '_do_' + command)()
        else:
            raise Exception


    def get(self, command, data=None):
        """Execture on client site"""
        if command in self.functions:
            # execute. What if server lags? idk
            # self.functions[command](*data)
            if data is not None:
                getattr(self, '_get_' + command)(data)
            else:
                getattr(self, '_get_' + command)()



    def __str__(self):
        """return name of user"""
        return self.username

    def __repr__(self):
        """return connection of user"""
        return self.connection
