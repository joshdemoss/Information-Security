import sys
from sys import argv

def read_and_reformat():
    charArr = list(sys.stdin.read().upper())
    charArr = filter(lambda x: x != '\n', charArr)
    return charArr

def encrypt(file, keyVal, val): 
	shift = ord(keyVal[0]) - 65
	j = 0

	for i in range(len(file)):
		j = j % len(key)
		shift = (ord(keyVal[j]) - 65)	
		cur = ord(file[i])
		if cur > 64 and cur < 91:
			cur = cur - 65 + (shift * val)
			cur = (cur % 26) + 65
			if cur < 0: cur += 26
			j+= 1
			file[i] = chr(cur)
	return file

def decrypt(file, keyVal):
	return encrypt(file, keyVal, -1)


#Read in key and firgure out shift number
key = 'a'
if len(argv) == 2: 
	key = argv[1].upper()
	print("".join(encrypt(read_and_reformat(), key, 1)))

if len(argv) == 3:
	key = argv[2].upper()
	if argv[1] == "-d":
		print("".join(decrypt(read_and_reformat(), key)))
	else:
		print(argv[1]," was not a valid flag. Try '-d' to decrypt")
		sys.exit()
