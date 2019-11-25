from pwn import *

context.log_level = "DEBUG"

target = process("./serv.py")

flag = ""
target.recvuntil("wisely!\n")

def xor(s1, s2):
    return ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))

for i in range(3):
    target.sendline(str(i+1))
    target.recvuntil("Exit\n")
    target.sendline("1")
    target.recvuntil("hex)?\n")
    ptxt = "0"*16 + "1"*16 + "0"*16
    target.sendline(ptxt.encode('hex'))
    target.recvuntil("<= ")
    ctxt = target.recvline().strip("\n").decode('hex')
    ctxt1 = ctxt[0:16]
    target.recvuntil("Exit\n")
    target.sendline("2")
    target.recvuntil("hex)?\n")
    new_ctxt = ctxt1 + "\x00"*16 + ctxt1
    target.sendline(new_ctxt.encode('hex'))
    target.recvuntil("<= ")
    new_ptxt = target.recvline().strip("\n").decode('hex')
    ptxt1 = new_ptxt[0:16]
    ptxt2 = new_ptxt[16:32]
    ptxt3 = new_ptxt[32:48]
    key = xor(ptxt1, ptxt3)
    flag += key
    target.recvuntil("Exit\n")
    target.sendline("3")
    target.recvline()

print flag
