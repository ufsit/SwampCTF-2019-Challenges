#!/usr/bin/env bash

nasm -f elf64 -o wetware.o wetware.asm
gcc -no-pie -fno-stack-protector -zexecstack -N -o wetware wetware.o -nostartfiles -nostdlib -nodefaultlibs
#strip wetware
