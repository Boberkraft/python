import rpyc

c = rpyc.connect('localhost', 18812)
bgsrv = rpyc.BgServingThread(c)

# function to receive messages
def get_msg(s):
    '''function for interacting with server'''
    print(s)


username = input('Your username: ')

# class for interracting with server
myself = c.root.ClientService(username, get_msg)

while True:
    where = input('To who: ')
    what = input('What: ')
    myself.send(where, what)

bgsrv.stop()
c.close()
