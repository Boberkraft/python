from user import User

class MyUser(User):
    access = {'msg', 'list_users', 'poke'}

    # ------------------ DEFINED FUNCTIONALITY -----------------------
    # at end you need to invoke self.server.send to send something to another user

    # structure of message
    # self.server.send(where, what, who)
    # :where -> name of destination user
    # :what -> ['command_name', info] where info can vary
    # :who -> who is sending this. Use self.

    def _do_msg(self, where, what):
        """Sends message to someone"""
        what = ['msg', {'who': str(self), 'what': str(what)}]
        self.server.send(where, what, self)

    def _get_msg(self, msg_data):
        msg_data = tuple(msg_data.items())
        self.functions['msg'](msg_data)

    def _do_list_users(self):
        """List every user"""
        # maybe i should return value directly to caller?
        what = ['list_users', tuple(list(self.server.usernames))]
        self.server.send(str(self), what, self)

    def _get_list_users(self, all_users):
        self.functions['list_users'](all_users)

    def _do_poke(self, where):
        """Pokes someone"""
        what = ['poke', str(self)]
        self.server.send(where, what, self)

    def _get_poke(self, all_users):
        self.functions['poke'](all_users)



    # -------------- END OF DEFINED FUNCTIONALITY -------------------
