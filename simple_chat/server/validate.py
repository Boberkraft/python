

class Validate:
    @staticmethod
    def check_client(info):
        data = {}

        data['username'] = info['username']
        data['msg'] = info['msg']
        if not data['username'] or not data['username'].isalnum():
            raise InvalidUsername('Please Change your username')

        if type(data['username']) != str:  # sorry for type checking :/
            raise AttributeError('Username is not a string')
        return data
