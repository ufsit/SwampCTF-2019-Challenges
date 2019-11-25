# import numpy as np 
# import scipy as sp 

print("Hello")
flag = 'flag{GR8_R0T4T3_M8}'
enc = ''
print(flag)


def enc(flag):
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

	print(enc)

def dec(flag):
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
		enc += newChr
		print(newChr)
		v+=1

	print(enc)

# fk_dwBL1WI&I(G%P='k