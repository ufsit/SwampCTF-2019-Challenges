# Function for converting decimal to binary 
def float_bin(number, places = 3): 
	whole, dec = str(number).split(".") 
	whole = int(whole) 
	dec = int (dec) 
	res = bin(whole).lstrip("0b") + "."

	for x in range(places): 
		whole, dec = str((decimal_converter(dec)) * 2).split(".") 
		dec = int(dec) 
		res += whole 
	return res 

def decimal_converter(num): 
	while num > 1: 
		num /= 10
	return num 

def IEEE754(n) : 

	# identifying whether the number 
	# is positive or negative 
	sign = 0
	if n < 0 : 
		sign = 1
		n = n * (-1) 
	p = 30

	# convert float to binary 
	dec = float_bin (n, places = p) 

	# separate the decimal part 
	# and the whole number part 
	whole, dec = str(dec).split(".") 
	whole = int(whole) 

	# calculating the exponent(E) 
	exponent = len(str(whole)) - 1
	exponent_bits = 127 + exponent 

	# converting the exponent from 
	# decimal to binary 
	exponent_bits = bin(exponent_bits).lstrip("0b") 

	# finding the mantissa 
	mantissa = str(whole)[1:exponent + 1] 
	mantissa = mantissa + dec 
	mantissa = mantissa[0:23] 

	# the IEEE754 notation in binary 
	final = str(sign) + str(exponent_bits) + mantissa 

	# convert the binary to hexadecimal 
	hstr = '%0*X' %((len(final) + 3) // 4, int(final, 2)) 

	# return the answer to the driver code 
	return (hstr) 

# Driver Code 
if __name__ == "__main__" : 
	print (IEEE754(29.5892)) 
	print (IEEE754(-263.3)) 
