# Credit to Ryan for the writeup on this technique and inspiration for this topic!

from subprocess import Popen
from subprocess import PIPE, STDOUT
import sys
import string

command = "perf stat -x : -e instructions:u ./future_fun 1>/dev/null"
flag = ''
while True:
    count = 0
    char_ = ''
    for i in string.printable:
        target = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
        target_output, _ = target.communicate(input='%s\n'%(flag + i))
        #print target_output
        instructions = int(target_output.split(':')[0])
        if instructions > count:
            char_ = i
            count = instructions
    flag += char_
    print flag
