import rpyc

class User():
    """Class for interacting with user"""
    def __init__(self, name, callback):
        self.callback = rpyc.async(callback)
        self.name = name
        self.active = True

    def send(self, who, msg):
        """sends a message to user"""
        print(self.name + ' is sending a message to ', who)
        message = '\n%-10s%s\n' % (who + ':', msg)
        self.callback(message)

    def __str__(self):
        return self.name

class ChatService(rpyc.SlaveService):

    connected = []

    class exposed_ClientService(object):

        def __init__(self, name, callback):
            self.add_user(name, callback)

        def add_user(self, name, callback):
            """Makes new user"""
            new_user = User(name, callback)
            # go to the list of all users
            ChatService.connected.append(new_user)

            self.user = new_user
            # list all logged users
            ChatService.list_users()

        def exposed_send(self, where, msg):
            """Sends a message. User - > User"""
            # finds addressee
            for user in ChatService.connected:
                if where == user.name:
                    user.send(user.name, msg)

    def list_users():
        """Lists all users"""
        end = 'Listing all users: '
        end += '['
        for user in ChatService.connected:
            end += str(user) + ', '
        end += ']'
        print(end)

    def stop_client(self):
        # number_of_clients = len(ChatService.connected)
        pass

    def stop_client(self):
        pass

    def on_connect(self):
        print('Someone connected')

    def on_disconnect(self):
        print('Someone disconnected')


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ChatService, port=18812)
    t.start()
