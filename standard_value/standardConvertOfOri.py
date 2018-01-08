"""
用途：将输入文件中的数据经过标准化处理（减去mean，在除以标准差）
"""
def printHelpInfo():
	print("""
Useful: 
		
	python standardConvertOfOri.py -i inputFilename -o outputFilename

		""")

def obtainNucleotidesPhysicoChemicalDict(filename):
	phychemdict = dict()
	phychems= []

	count_line = 0
	f = open(filename)
	for eachline in f:
		count_line += 1
		temp = eachline.strip().split("\t")
		if count_line == 1:
			noteline = eachline
			nucleotides = temp[1:]
		else:
			phychems.append(temp[0])
			phychemdict[temp[0]] = dict()
			count_num = 0
			for each in temp[1:]:
				count_num += 1
				phychemdict[temp[0]][nucleotides[count_num-1]] = float(each)
	f.close()

	return phychemdict, nucleotides, phychems, noteline


def calculateStandardConvertedValue(phychemdict):
	standValueDict = dict()
	for eachkey in phychemdict.keys():
		standValueDict[eachkey] = dict()

		temp = phychemdict[eachkey]
		value_array = np.array(list(temp.values()))
		value_mean = float('%.3f'%value_array.mean())
		value_std = float('%.3f'%value_array.std())

		for each in temp.keys():
			standValueDict[eachkey][each] = (temp[each]-value_mean)/value_std 

	return standValueDict

def generateResultFileIncludingStandardValue(out_file):
	[phychemdict, nucleotides, phychems, noteline] = obtainNucleotidesPhysicoChemicalDict(in_filename)
	standValueDict = calculateStandardConvertedValue(phychemdict)

	sequence = noteline
	for eachPhyChem in phychems:
		sequence += eachPhyChem
		for eachNucle in nucleotides:
			sequence += "\t%.3f"%standValueDict[eachPhyChem][eachNucle]
		sequence += "\n"

	g = open(out_file, 'w')
	g.write(sequence)
	g.close()

import sys
import numpy as np

try:
	if sys.argv[1] == "-i":
		in_filename = sys.argv[2]
	else:
		assert 0

	if sys.argv[3] == "-o":
		out_filename = sys.argv[4]
	else:
		assert 0
except:
		printHelpInfo()
		exit(0)

if __name__ == '__main__':

	try:
		generateResultFileIncludingStandardValue(out_filename)
	except:
		printHelpInfo()



