# [SwampCTF 2019 Reversing] Future Fun

## Flavor Text

Deep on the web, I discovered a secret key validation. It appeared to be from the future, and it only had one sentence:
"Risk speed for security". Something seems fishy, you should try to break the key and find the secret inside!

* Flag: flag{g00d_th1ng5_f0r_w41ting}
* Expected difficulty: hard 

## Description

This challenge is supposed to teach the participants about the use of side channel attacks for reverse engineering.
A timing attack will work in solving this challenge, and I added extra loops to make this more reliable.
People should notice that the binary is obfuscated, and they should recognize to try side channel attacks before static analysis.

## Challenge Solution
The solution to this challenge is to perform a byte-by-byte brute force based on perf log.
Any other side channel attack could work as well, but the number of instructions performed was proven to work.
A script should test each byte and see which results in the most instructions performed. This byte is appended to the flag so far.
The script could theoretically run forever, but the flag will be complete once the closing "}" is found.
An example script that would perform this side channel attack is included in src/ .
Also of note, the side channel attack with perf only works if the CPU allows for perf to use instructions. This does not work on my host but does on my digital ocean server.
