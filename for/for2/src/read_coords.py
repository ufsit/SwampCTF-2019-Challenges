import struct
import binascii
import xlwt 
from xlwt import Workbook 

wb = Workbook() 
sheet1 = wb.add_sheet('Sheet 1') 

f = open("coord_text.txt", "r")

t = open("ip_addresses.txt","w")


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def hex_to_float(f):
    hS = str(f) 
    return float(struct.unpack('>f', binascii.unhexlify(f[2:]))[0])

def hex_to_IP(f):
	hexP = f[2:]
	print(type(hexP))
	print(int(hexP[0:2],16))
	return ("{}.{}.{}.{}".format(int(hexP[0:2],16),int(hexP[2:4],16),int(hexP[4:6],16),int(hexP[6:8],16)))


# output = float_to_hex(-82.3151)    # Output: '0x418c0000'
# print (output)

v = 0
for x in f:
	
	print(" ")
	print(v)
	print("-----")
	# print(x)
	splitS = x.split("\t")
	f0 = float(splitS[0])
	h0 = float_to_hex(f0)
	hf0 = hex_to_float(h0)
	ip = hex_to_IP(h0)
	print (f0, " = ",h0," = ",hf0, " = ",ip)
	t.write(ip)
	t.write("\n")
	sheet1.write(v,1,hf0)

	f1 = float(splitS[1])
	h1 = float_to_hex(f1)
	hf1 = hex_to_float(h1)
	ip1 = hex_to_IP(h1)
	print (f1, " = ",h1," = ",hf1, " = ",ip1)
	t.write(ip1)
	t.write("\n")
	sheet1.write(v,2,hf1)

	v+=1

wb.save('xlwt example2.xls')
t.close()