#!/usr/bin/env bash

nasm -f elf64 -o wetware_hardened.o wetware_hardened.asm
gcc -no-pie -fno-stack-protector -N -z noexecstack -o wetware_hardened wetware_hardened.o -nostartfiles -nostdlib -nodefaultlibs
#strip wetware
