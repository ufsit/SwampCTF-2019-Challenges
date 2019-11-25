with open("translation_text.txt") as fileobj: 
	for line in fileobj: 
			print(line)
with open("translation_text.txt") as fileobj: 	
	for line in fileobj: 
		for ch in line:
			if (ch=='a'):
				# print(ch)
				ch = 'f'
				print(ch,end="")
			if (ch=='b'):
				ch = 'm'
				print(ch,end="")
			if (ch=='c'):
				ch = 'j'
				print(ch,end="")
			if (ch=='d'):
				ch = 'd'
				print(ch,end="")
			if (ch=='e'):
				ch = 'i'
				print(ch,end="")
			if (ch=='f'):
				ch = ''
				print(ch,end="")
			# if (ch=='g'):
			# if (ch=='h'):
			# if (ch=='i'):
			# if (ch=='j'):
			# if (ch=='k'):
			# if (ch=='l'):
			# if (ch=='m'):
			# if (ch=='n'):
			# if (ch=='o'):
			# if (ch=='p'):
			# if (ch=='q'):
			# if (ch=='r'):
			# if (ch=='s'):
			# if (ch=='t'):
			# if (ch=='u'):
			# if (ch=='v'):
			# if (ch=='w'):
			# if (ch=='x'):
			# if (ch=='y'):
			# if (ch=='z'):
			# if (ch=='a'):
			# if (ch==' '):
				# print(ch,end="")
			# if (ch=='a'):
				# print(ch,end="")
			else:
				print(ch,end="")

# with open("block_test_for_2FA.txt") as fileobj:
#     for line in fileobj:  
#        for ch in line: 

#            if (ch == 'a'):
#            	print (ch)
