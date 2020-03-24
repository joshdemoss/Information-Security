import sys
import numpy as np
import math
import crypt

letterFrequency = [8.12, 1.49, 2.71, 4.32, 12.0, 2.30, 2.03, 5.92, 7.31, 0.10, 
				0.69, 3.98, 2.61, 6.95, 7.68, 1.82, 0.11, 6.02, 6.28, 9.1, 2.88,
				1.11, 2.09, 0.17, 2.11, 0.07]
freqArr  = [letterFrequency]
for i in range(1, 26):
	freqArr.append(np.roll(letterFrequency, i))
# print(len(freqArr))
# print(freqArr[0], freqArr[1])


def read_and_reformat():
    charArr = list(sys.stdin.read().upper())
    charArr = filter(lambda x: 'A' <= x <= 'Z', charArr)
    return charArr

def countCharsInSLice(file, keySize, startI):
	count = np.array([float(0)] * 26)
	length = 0
	realI = 0
	i = startI
	for i in range(i, len(file)):
		letterI = ord(file[i]) - 65 		#get cur letter as 0-26
		
		if letterI > -1 and letterI < 26:	#if valid letter &
			if (realI % keySize) == 0:		#if looking at cur slice
				count[letterI] += 1			#count that letter
				length += 1					#increase the length
				# print(realI, file[i]) 		
			realI += 1

	assert np.sum(count) == length
	return count, length


def correlation(count, length):
	for i in range(len(count)):					#convert count to percentages
		count[i] = count[i]/length * 100

	bestR = np.corrcoef(count, letterFrequency)[0][1]
	for i in range(1, 26):
		curR = np.corrcoef(count, freqArr[i])[0][1] #find curR between count of cur slice and freqs
		if curR > bestR:
			bestR = curR
	return bestR

def findKeySize(file, maxKey):
	minR = 0
	lKeySize = 1
	keySize = 1
	while keySize <= maxKey:
		print("\nKeySize: "+str(keySize))
		
		sumR = 0
		for curKey in range(2):					#change this to keysize if you want better accuracy
			count, length = countCharsInSLice(file, keySize, curKey)
			foundR = correlation(count, length)
			sumR += foundR		
		avgR = sumR / 2

		if avgR > minR: 			#check count of current slice
			minR = avgR			#if better store minR, lKeySize
			lKeySize = keySize
		
		if avgR > .8:
			print("Met Requirement! r: "+str(minR))
			return lKeySize		
		keySize += 1

	print("Couldn't find a key with r < 0.8 However, the best keySize was " + str(lKeySize)
			+ " with r = " + str(minR)+ " I will try that for you!")
	return lKeySize


def findKey(file, maxKey):
	keySize = findKeySize(file, maxKey)
	if keySize == 0: return None

	print("keySize:", keySize)
	
	lCounts = []
	for i in range(0, keySize): 
		curCount = countCharsInSLice(file, keySize, i)[0] 	# adding counts of those slices
		lCounts.append(curCount)		#add them all to the list to keep track of them

	key = ""
	for i in lCounts:					#go through list and find char for each letter
		curKey = findCeasarKey(i)
		key += curKey					#add keys together
	return key

def findCeasarKey(count):
	bestE = np.corrcoef(count, freqArr[0])[0][1]
	shift = 0
	for i in range(26): 				#test all shifts and see which one matches up most
		curE = np.corrcoef(count, freqArr[i])[0][1]
		if curE > bestE:
			bestE = curE
			shift = i
	key = chr(shift + 65)
	return key

print(findKey(read_and_reformat(), 1000))