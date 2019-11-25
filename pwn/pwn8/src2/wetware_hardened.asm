BITS 64
GLOBAL _start
_start:

;stack frame
push rbp
mov rbp, rsp
sub rsp, 0x200

;lets print message: rdi and rdx already set!
print:
mov rdi, 1
mov rsi, msg1
mov rdx, 0x27
mov rax, 1
syscall

;now read input 1 byte at a time:
mov rsi, rsp
read:
mov rax, 0
mov r10, rsp
add r10, 0x200
mov rdi, 0
mov rdx, 1
syscall

;compare to \x00 or \x0a
cmp byte [rsi], 0
jz decode
cmp byte [rsi], 0xa
jz decode
cmp rsi, r10
jge exit1
inc rsi
jmp read

;exit
decode:
mov rsi, rsp  ;key
mov rdi, msg2 ;data
xor rcx, rcx
xor rdx, rdx
loop:
mov bl, byte [rsi+rcx]
xor byte [rdi], bl
inc rdi
cmp rcx,5
jz res
inc rcx
jmp loop

res:
xor ecx, ecx
cmp rdx, 11
jz msg2
inc rdx
jmp loop


exit1:
db 0xb0,0x3c,0x48,0x31,0xff,0x0f,0x05

txt1:
db 0x48,0x31,0xc0

msg1:
db 'Holographic demux codephrase required: ',0x27

msg2:
;incbin "dump_hardened.bin"
incbin "dump_hardened2.bin"

;mov rdi, 1
;mov rsi, msg3
;mov rdx, 38
;mov rax, 1
;syscall
;db 0xb0,0x3c,0x48,0x31,0xff,0x0f,0x05
;msg3:
;db 'Gain access by self-reflecting, johnny',42
;db 'The datacore can be unlocked by self-reflection, johnny',56
