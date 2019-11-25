# [SwampCTF 2019 Pwn] Heap Golf 2

## Flavor Text

So you come back to try your hand again? Think you can point to the right chunk?
NOTE: ASLR is disabled. 


* Flag: **[TODO: Enter the challenge flag here]**
* Expected difficulty: medium 

## Description

Effectively the spiritual successor to the first heap golf problem. There is a list on top of the heap that holds pointers to all the heap chunks the player can allocate. It also keeps track of a function pointer, which is always at the end of this heap list. Whenever the player allocates, the function pointer is moved down on step, then the newly allocated heap pointer replaces it. This heap pointer list is not checked for size, so the player can allocate as many chunks on the heap as they want. This overflows the heap pointers into the closest chunk to them on the heap. Normally, that would corrupt the size value of the nearest chunk and that would be all she wrote. However, if the player applies knowledge from the previous challenge, they can flip the order that chunks are allocated on the heap. This way the function pointer at the top of the pointer list on the heap is passed down into a free region of memory, which the player can subsequently allocate and then overwrite, allowing for code execution.

NOTE: This challenge should have ASLR disabled, so that the player can jump to the win function without needing to leak memory. (they can if they wish to using the read functionality. This will crash the program though. However, with ASLR off there pointer should still function after the crash.) 


## Challenge Solution

First off, allocate 2 fast bins and free them. I stick AA in them just to know who they are when I examine memory
25
AA
25
AA

Then free them both with -2
-2

now allocate one
25
AA

This will leave a fastbin sized space in memory between the allocated fast bin and the list of heap pointers.

now allocate as many large size bins as neccessary to increment the function pointer at the top of the heap list into the empty fast bin space

200 (12 times)
BB

allocate the fast bin on top of the heap chunk and use a pwntools to pass in the hex for the win functions location
25
hex hex hex

then exit with -1 (which calls the function pointer at the top of the heap list without freeing anything :) )
-1

