def printHelpInfo():
	print("""
Useful: 
		
	python PseKNC.py -t 1/2 -w 0.05 -r 100 -i inputFilename -o outputFilename

  parameter description:

	-t: The type of PseKNC. 1 -> Type 1 PseKNC[default]; 
							2 -> Type 2 PseKNC.(only this)

	-w: The weight factor for the sequence order effect and used to put weight to the additional pseudo nucleic acid components with respect to the conventional nucleic acid components. The users are allowed to select the weight factor from 0.1 to 1.0 . The default is 0.5.

	-r: It represents the counted rank (or tier) of the correlation along a DNA sequence. It must be non-Negative integer and smaller than L-k. 

	-i: The input filename. (required)

	-o: The output filename. (required)

		""")
	exit(0)

def detectingPythonVersionAndOutputHelpInfo():
	if sys.version[0] == '2':
		print("""\nVersionError: The current python version: '%s',
		You must use python version 3 or later to run this script!\n"""%((sys.version).split('\n')[0]))
		exit(0)
	else:
		pass

	try:
		if sys.argv[1] == "--help":
			printHelpInfo()
		else:
			pass
	except:
		printHelpInfo()

def obtainExternalParameters():
	try:
		if sys.argv[1] == "-t":
			typeOfPseKNC = int(sys.argv[2])
		else:
			assert 0
		if sys.argv[3] == "-w":
			weightFactor = float(sys.argv[4])
		else:
			assert 0
		if sys.argv[5] == "-r":
			lambdaPara = int(sys.argv[6])
		else:
			assert 0
		if sys.argv[7] == "-i":
			in_filename = sys.argv[8]
		else:
			assert 0
		if sys.argv[9] == "-o":
			out_filename = sys.argv[10]
		else:
			assert 0
	except:
			printHelpInfo()
	return typeOfPseKNC, weightFactor, lambdaPara, in_filename, out_filename


def obtainNucleotidesPhysicoChemicalDict(filename):
	phychemdict = dict()
	phyChemList = []

	count_line = 0
	f = open(filename)
	for eachline in f:
		count_line += 1
		temp = eachline.strip().split("\t")
		if count_line == 1:
			nucleotides = temp[1:]
		else:
			phyChemList.append(temp[0])
			phychemdict[temp[0]] = dict()
			count_num = 0
			for each in temp[1:]:
				count_num += 1
				phychemdict[temp[0]][nucleotides[count_num-1]] = float(each)
	f.close()

	return phychemdict, nucleotides, phyChemList


def generateCsvFormatLinebyType1PseKNC(in_file, out_file, numConjoin, weightFact, lambdaPara, nucleoStandDict, nucleotides, phyChemList):
	pass


def calculateFeatureValueByCorrFactorsDictAndOccurfrequencyType2(corrFactorsDict, occurfrequency, weightFact, lambdaPara, nucleotides, phyChemList):
	featureValueStr = ''

	corrSum = 0
	for eachkey in phyChemList:
		corrSum += sum(corrFactorsDict[eachkey].values())
	corrPart = corrSum*weightFact
	
	for eachNuc in nucleotides:
		featureValueStr += ',%.6f'%(occurfrequency[eachNuc]/(1+corrPart))

	for i in range(lambdaPara):
		for phyChemKey in phyChemList:
			featureValueStr += ',%.6f'%((weightFact*corrFactorsDict[phyChemKey][i+1])/(1+corrPart))

	return featureValueStr+'\n'

def calculateOccurenceFrequencyOfOlinucletide(kTuples, nucleotides):
	occurfrequency = dict()
	tupleLen = len(kTuples)
	for each in nucleotides:
		occurfrequency[each] = kTuples.count(each)/tupleLen
	
	return occurfrequency

def calculateAllCorrelationFactorAndOccurenceFrequencyType2(sequence, numConjoin, nucleoStandDict, nucleotides, phyChemList):
	corrFactorsDict = dict()

	seqLen = len(sequence)
	kTuples = []  # All twins in a sequence
	for i in range(seqLen-numConjoin+1):
		kTuples.append(sequence[i:i+numConjoin])

	occurfrequency = calculateOccurenceFrequencyOfOlinucletide(kTuples, nucleotides)


	for eachName in phyChemList:
		corrFactorsDict[eachName] = dict()
		for lamPa in range(1,(lambdaPara+1)):
			temp = []
			for kTuplesIndex in range(len(kTuples)-lamPa):
				preKTuple = kTuples[kTuplesIndex]
				backKTuple = kTuples[kTuplesIndex+lamPa]
				try:
					tempNumber = nucleoStandDict[eachName][preKTuple]*nucleoStandDict[eachName][backKTuple]
					temp.append(tempNumber)
				except:
					continue

			corrFactorsDict[eachName][lamPa] = sum(temp)/len(temp)

	return corrFactorsDict, occurfrequency


def generateCsvFormatNoteLineType2(numConjoin, lambdaPara, nucleotides, phyChemList):
	noteLine = 'class'
	for eachNuc in nucleotides:
		noteLine += ",%s_f"%(eachNuc)

	for i in range(lambdaPara):
		for eachName in phyChemList:
			noteLine += ",%s_%d"%(eachName,(i+1))

	return noteLine+'\n'


def generateCsvFormatLinebyType2PseKNC(in_file, out_file, numConjoin, weightFact, lambdaPara, nucleoStandDict, nucleotides, phyChemList):
	g = open(out_file,'w')
	g.write(generateCsvFormatNoteLineType2(numConjoin, lambdaPara, nucleotides, phyChemList))
	g.close()

	f = open(in_file)
	count_line = 0
	for eachline in f:
		if eachline[0] == '>':
			count_line += 1
#print("  Calculating: sequence-%d"%count_line)
			sampleType = re.findall(r'@(\d)@', eachline)[0]
		else:
			sequence = eachline.strip()
			[corrFactorsDict, occurfrequency] = calculateAllCorrelationFactorAndOccurenceFrequencyType2(sequence, numConjoin, nucleoStandDict, nucleotides, phyChemList)
			tempLine = calculateFeatureValueByCorrFactorsDictAndOccurfrequencyType2(corrFactorsDict, occurfrequency, weightFact, lambdaPara, nucleotides, phyChemList)
			g = open(out_file,'a')
			g.write("%s%s"%(sampleType,tempLine))
			g.close()

	f.close()

import re
import sys

detectingPythonVersionAndOutputHelpInfo()
[typeOfPse, weightFact, lambdaPara, in_file, out_file] = obtainExternalParameters()

numConjoin = 2

if __name__ == '__main__':
	diNcleoStandFile = r'./standard_value/dinucleotides_11_standardRNA.txt'
	[nucleoStandDict, nucleotides, phyChemList] = obtainNucleotidesPhysicoChemicalDict(diNcleoStandFile)

	if typeOfPse == 1:
		generateCsvFormatLinebyType1PseKNC(in_file, out_file, numConjoin, weightFact, lambdaPara, nucleoStandDict, nucleotides, phyChemList)
	elif typeOfPse == 2:
		generateCsvFormatLinebyType2PseKNC(in_file, out_file, numConjoin, weightFact, lambdaPara, nucleoStandDict, nucleotides, phyChemList)
	else:
		printHelpInfo()

	print("------Finished!------")
