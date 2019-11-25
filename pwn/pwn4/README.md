# [SwampCTF 2019 Pwn] Heap Golf

## Flavor Text

Don't play golf. It's heaps and heaps of trouble getting stuff where ya want it...

* Flag: `flag{Gr34t_J0b_t0ur1ng_0ur_d1gi7al_L1nk5}`
* Expected difficulty: easy

## Description

This challenge teaches about heap organization and how bins are constructed. Basically, it's important to know how free bins are stored in the bin lists. This challenge is pretty easy but builds skills so players can move onto heap glof 2.


## Challenge Solution

The key part of this challenge is to note that fast bins are free'd and then reallocated in reverse order (the fast free bin is a FILO order, unlike the other bins. This allows the challenger to allocate 5 fastbin chunks on the heap, then free them, then reallocate them, forceing the 5th bin to be at the location the first was at originally. In this challenge, heap chunks are numbered with a index. Upon exiting, the program checks the bin at the lowest location in memory for the index 5. If it has 5, it jumps to a win function.

25
25
25
25
-2
25
25
25
25
^^ this is the simplest solution to get the flag.
