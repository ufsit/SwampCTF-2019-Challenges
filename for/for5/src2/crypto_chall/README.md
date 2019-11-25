# [SwampCTF 2019 Forensics] Hot and Cold (never released)

## Flavor Text

EvilCorp's biostorage center security systems are some of the hardest things to crack. We managed to intercept what we think is a key that should help us in gaining access. Luckily we have you on our side, you'll be able to crack it, won't you? 

* Flag: flag{GR8_R0T4T3_M8}
* Expected difficulty: easy

## Description
User will try typical ciphers first then eventually try and rotate each letter at a time. Once the player understands each character is being decremented then we can write a script that does is automatically. Once they reach the 5th character the decrementing by 1 won't work anymore, but we know that { is supposed to be the 5th character. Doing the math it seems like our ascii displacement is now +5 instead of just +1. Therefore, we can then assume that every 5th character is having 5 more added to its offset. After they see the pattern of rotation they will get the flag.

## Challenge Solution
```
def decode(flag):

	dec = ''
	v = 0 
	for x in flag:
		print(x," = ",end = "")
		init = ord(x)=
		if (v+1 % 5 == 0):
			v += 5
		newChr = chr(init + v)
		dec += newChr
		print(newChr)
		v+=1
	return dec
```
