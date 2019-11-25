import struct
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

output = 	float_to_hex(-82.3151)    # Output: '0x418c0000'
print (output)
