import subprocess
import re
import threading
import shlex
import sys
import time

try:
    from colorconsole import terminal

    screen = terminal.get_terminal(conEmu=False)
except ImportError:
    class screen:
        @staticmethod
        def cprint(a, b, *args ):
            print(*args)

        @staticmethod
        def reset_colors():
            pass

def ex():
    if not len(sys.argv) > 1:
        input('Press ENTER to continue\n')
    sys.exit()


class IpCheck(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.response = ''
        self.received = []
        self.ip = ip
        self.r = re.compile(r'\(.*\)')

    def run(self):
        cmd = shlex.split('ping ' + self.ip)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        received = process.stdout.read()
        self.received = str(received)
        self.gen_response()

    def gen_response(self):
        response = self.r.findall(self.received)
        self.response = [self.ip, str(response)[2:-2]]


class Checker:
    th_pings = []

    def __init__(self, ip, start, end, succ):
        if not ip.endswith('.'):
            ip += '.'
        self.ip = ip
        self.succ = succ
        self.start = int(start)
        self.end = int(end)
        self.run()

    def run(self):
        global screen
        print('Pinging in range ' + self.ip + str(self.start) + ' - ' + self.ip + str(self.end) + '...')
        for suffix in range(self.start, self.end + 1):

            th = IpCheck(self.ip + str(suffix))
            th.daemon = True
            th.start()
            self.th_pings.append(th)

        try:
            x = 0
            for process in self.th_pings:
                while process.is_alive():
                    process.join(0.1)
                    print('\r' + '#' * x, end='')
                    x += 1
                    if x > 10:
                        print('\r' + ' ' * (x - 1), end='')
                        x = 0
        except KeyboardInterrupt:
            ex()
        print('\n')

        for process in self.th_pings:
            color = 0
            if process.response[1].find('100%') != -1:
                if self.succ:
                    continue
                color = 12
            elif process.response[1].find('(0%') != -1:
                color = 10
            else:
                color = 14
            screen.cprint(color, 0, process.response[0] + ' ')
            screen.cprint(color, 0, process.response[1])
            screen.reset_colors()
            print()




succ = False
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg == '-h' or arg =='--help' or arg == 'help' or arg == "?":
            print('Usage: pingth.exe ip start end [--succ]')
            print()
            print('\tip\t first 3 octects in your address')
            print('\tstart\t first address to ping')
            print('\tend\t last address to ping')
            print()
            print('Options:\n')
            print('\t--succ\tdon\'t show unsuccessful pings')
            print()
            print('Example usage:\n')
            print('\tpingth 192.168.1 1 254\tpings every address from 1 to 254')
            ex()

    ip = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    if '--succ' in sys.argv:
        succ = True

else:
    ip = input("Ip address 0.0.0 : ")
    start = input('start: ')
    end = input('end: ')
try:
    start, end = int(start), int(end)
except ValueError as er:
    print('Start or End must be a number!')
    ex()

# ip = '192.168.1'
# start = 1
# end = 254

check = Checker(ip, start, end, succ)

ex()
