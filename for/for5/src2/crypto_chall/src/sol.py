# import numpy as np 
# import scipy as sp 

# print("Hello")
f = 'flag{GR8_R0T4T3_M8}'
# print(flag)


def encode(flag):
	enc = ''

	v = 0 
	for x in flag:
		print(x," = ",end = "")
		init = ord(x)
		# if (x == '{' or x=='}'):
			# print (chr(ord(x)+v))
			# print(ord(x))
		if (v+1 % 5 == 0):
			v += 5
		newChr = chr(init - v)
		enc += newChr
		print(newChr)
		v+=1

	return enc

def decode(flag):
	dec = ''

	v = 0 
	for x in flag:
		print(x," = ",end = "")
		init = ord(x)
		# if (x == '{' or x=='}'):
			# print (chr(ord(x)+v))
			# print(ord(x))
		if (v+1 % 5 == 0):
			v += 5
		newChr = chr(init + v)
		dec += newChr
		print(newChr)
		v+=1

	return dec


cipher = encode(f)
print(cipher)
dec = decode(cipher)
print(dec)
# fk_dwBL1WI&I(G%P='k