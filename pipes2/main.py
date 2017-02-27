import subprocess
import shlex

import logging
from logging import debug
logging.basicConfig(level=logging.DEBUG, format='%(module)s - %(message)s')
num_tries = 0

class Guesser():
    def __init__(self, cmd, where=(0, 200)):
        cmd = shlex.split(cmd)
        self.where = where
        self.p = subprocess.Popen(cmd,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  universal_newlines=True)

    def start(self):
        self.send('{} {}'.format(self.where[0], self.where[1]))

    def send(self, num):
        print(num, file=self.p.stdin, flush=True)

    def get(self):
        for output_line in self.p.stdout:
            yield int(output_line)
        self.p.stdout.close()
        return_code = self.p.wait()
        if return_code:
            raise IOError("Guesser returned error")

    def end(self):
        pass

if __name__ == '__main__':
    my_hidden_number = 100
    # program_name = input("Enter program name:")
    program_name = 'wojtek.exe'
    guesser = Guesser(program_name, (0, 100))
    guesser.start()
    debug('Starowanie się powiodło')
    for output in guesser.get():
        num_tries += 1
        debug('Dobra pierwsze zgadywanie: ' + str(output))
        print('he guessed', output)
        if output > my_hidden_number:
            guesser.send('-1')
        elif output < my_hidden_number:
            guesser.send('1')
        elif output == my_hidden_number:
            guesser.send('0')
            break
        debug('wysyłam odp.')
print('got in %i tries' % num_tries)

