# Vigenere Decipher
# Joshua DeMoss

import sys
import numpy as np
import math
import crypt

# A list of letter frequencies -- in order so that letterFrequency[0] corresponds to A and letterFrequency[25] corresponds to Z
letterFrequency = [8.12, 1.49, 2.71, 4.32, 12.0, 2.30, 2.03, 5.92, 7.31, 0.10, 
				0.69, 3.98, 2.61, 6.95, 7.68, 1.82, 0.11, 6.02, 6.28, 9.1, 2.88,
				1.11, 2.09, 0.17, 2.11, 0.07]

# Get a list of lists -- each one being a letter frequency list in alphabetical order, but starting with a different letter
# So after this, freqArr[0][0] is the frequency of A, freqArr[0][1] is freq of B, freqArr[1][0] is freq of B, and freqArr[1][1]
# is freq of C
freqArr  = [letterFrequency]
for i in range(1, 26):
	freqArr.append(np.roll(letterFrequency, i))

# helper method to read text while transforming read characters into capital ones -- then get rid of non A-Z characters
def read_and_reformat():
    charArr = list(sys.stdin.read().upper())
    charArr = filter(lambda x: 'A' <= x <= 'Z', charArr)
    return charArr

# Take a slice of the text depending on key size and store the freq of each character in an array
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

# Turn the freq of each character in the count array into percentages and find the correlation coefficient for the array 
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
	# Iterate through every possible key size and examine how well the character frequency holds up.
	# Return early if the accuracy is above a certain threshhold, otherwise return key size with the highest accuracy
	while keySize <= maxKey:
		print("\nKeySize: "+str(keySize))
		
		sumR = 0
		# How many different slices of the same key size do we want to examine to get an accurate result
		# 2 seems to work okay, but we could make it keysize to get most accuracy.
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

# Get the most likely keysize, then divide text in to keysize slices, and do ceasar cipher on each slice to figure out
# the encoding character. Then return the key that was discovered. This can be used separately to now decrpyt the encrpyted text.
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

# A simple ceaser cipher decription method -- checks every letter to see which letter is the key -- uses character freq analysis 
# to check correlation coefficient.
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
