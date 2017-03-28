import rpyc

c = rpyc.connect('localhost', 18812)
bgsrv = rpyc.BgServingThread(c)


def get_msg(s):
    """function to receiving messages"""
    print(s)

def ping():
    """ping pong he"""
    # kop bitcoiny
    return 'pong'


communication = {
    'ping': ping,
    'get_msg': get_msg
}

username = input('Your username: ')

# class for interacting with server
myself = c.root.connect(username, communication)

while True:
    where = input('To who: ')
    what = input('What: ')
    myself.send_msg(where, what)

bgsrv.stop()
c.close()
