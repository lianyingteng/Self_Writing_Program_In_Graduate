def printHelpInfo():
	print("""
Useful: 
		
	python PseAAC.py -t 1/2 -w 0.05 -r 100 -i inputFilename -o outputFilename

  parameter description:

	-t: The type of PseAAC. 1 -> Type 1 PseAAC[default]; 
							2 -> Type 2 PseAAC.(Only this)

	-w: The weight factor for the sequence order effect and used to put weight to the additional pseudo nucleic acid components with respect to the conventional nucleic acid components. The users are allowed to select the weight factor from 0.1 to 1.0 . The default is 0.5.

	-r: It represents the counted rank (or tier) of the correlation along a protein sequence. It must be non-Negative integer and smaller than L-1. 

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

def argsParser():
	"""参数获取
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-t",
		type=int,
		default=2,
		help="PseAAC类型 【超参数】"
		)
	parser.add_argument(
		"-w",
		type=float,
		default=0.5,
		help="伪组分权重 【超参数】"
		)
	parser.add_argument(
		"-r",
		type=int,
		default=30,
		help="lambda参数 【超参数】"
		)
	parser.add_argument(
		"-i",
		type=str,
		default="mergeSampleFile.txt",
		help="蛋白序列文件 【输入】"
		)
	parser.add_argument(
		"-o",
		type=str,
		default="output_CSV.csv",
		help="输出结果文件csv 【输出】"
		)
	args = parser.parse_args()
	return args.t, args.w, args.r, args.i, args.o


def detectingTheRationalityOfLambdaPara(in_file, lambdaPara):
	seqLens = []

	f = open(in_file)
	for eachline in f:
		if eachline[0] == ">":
			pass
		else:
			seqLens.append(len(eachline.strip('\n')))

	seqMinLen = min(seqLens)
	if lambdaPara > (seqMinLen-1):
		print("Parameter Error : The Lambda Parameter must smaller than L-1!")
		exit(0)




def obtainAminoAcidPhysicoChemicalDict(filename):
	phychemdict = dict()
	phyChemList = []

	count_line = 0
	f = open(filename)
	for eachline in f:
		count_line += 1
		temp = eachline.strip().split("\t")
		if count_line == 1:
			aminoAcid = temp[1:]
		else:
			phyChemList.append(temp[0])
			phychemdict[temp[0]] = dict()
			count_num = 0
			for each in temp[1:]:
				count_num += 1
				phychemdict[temp[0]][aminoAcid[count_num-1]] = float(each)
	f.close()

	return phychemdict, aminoAcid, phyChemList


def generateCsvFormatLinebyType1PseAAC(in_file, out_file, weightFact, lambdaPara, phyChemDict, aminoAcid, phyChemList):
	pass


def generateCsvFormatNoteLineType2(lambdaPara, aminoAcid, phyChemList):
	noteLine = 'class'
	for eachAA in aminoAcid:
		noteLine += ",%s_f"%(eachAA)

	for i in range(lambdaPara):
		for eachName in phyChemList:
			noteLine += ",%s_%d"%(eachName,(i+1))
	return noteLine+'\n'

def obtainSequenceAllDiAAC(sequence):
	content = []
	for i in range(len(sequence)-1):
		content.append(sequence[i:i+2])
	return content

def calculateOccurenceFrequencyOfAminoAcid(sequence, diAAC):
	occurfrequency = dict()
	sequences = obtainSequenceAllDiAAC(sequence)
	
	seqLen = len(sequences)
	for each in diAAC:
		eachCount = sequences.count(each)
		if eachCount == 0:
			occurfrequency[each] = 0
		else:
			occurfrequency[each] = eachCount/seqLen
	
	return occurfrequency


def calculateAllCorrelationFactorAndOccurenceFrequencyType2(sequence, phyChemDict, lambdaPara, aminoAcid, phyChemList, diAAC):
	corrFactorsDict = dict()

	occurfrequency = calculateOccurenceFrequencyOfAminoAcid(sequence, diAAC)

	for eachName in phyChemList:
		corrFactorsDict[eachName] = dict()
		for lamPa in range(1,(lambdaPara+1)):
			temp = []
			for resideIndex in range(len(sequence)-lamPa):
				preAA = sequence[resideIndex]
				backAA = sequence[resideIndex+lamPa]
				try:
					tempNumber = phyChemDict[eachName][preAA]*phyChemDict[eachName][backAA] # correlation function
					temp.append(tempNumber)
				except:
					continue

			corrFactorsDict[eachName][lamPa] = sum(temp)/len(temp)

	return corrFactorsDict, occurfrequency


def calculateFeatureValueByCorrFactorsDictAndOccurfrequencyType2(corrFactorsDict, occurfrequency, weightFact, lambdaPara, aminoAcid, phyChemList, diAAC):
	featureValueStr = ''

	corrSum = 0
	for eachkey in phyChemList:
		corrSum += sum(corrFactorsDict[eachkey].values())
	corrPart = corrSum*weightFact
	
	for eachAA in diAAC:
		featureValueStr += ',%.6f'%occurfrequency[eachAA]

	for i in range(lambdaPara):
		for phyChemKey in phyChemList:
			featureValueStr += ',%.6f'%((weightFact*corrFactorsDict[phyChemKey][i+1])/(1+corrPart))

	return featureValueStr+'\n'


def generateDiaminoAcidComposition(aminoAcid):
	content = []
	for i in aminoAcid:
		for j in aminoAcid:
			content.append(i+j)
	return content

def generateCsvFormatLinebyType2PseAAC(in_file, out_file, weightFact, lambdaPara, phyChemDict, aminoAcid, phyChemList):
	diAAC = generateDiaminoAcidComposition(aminoAcid)

	g = open(out_file,'w')
	g.write(generateCsvFormatNoteLineType2(lambdaPara, diAAC, phyChemList))
	g.close()

	f = open(in_file)
	count_line = 0
	for eachline in f:
		if eachline[0] == '>':
			count_line += 1
			sampleType = re.findall(r'@(\d)@', eachline)[0]
		else:
			sequence = eachline.strip()
			[corrFactorsDict, occurfrequency] = calculateAllCorrelationFactorAndOccurenceFrequencyType2(sequence, phyChemDict, lambdaPara, aminoAcid, phyChemList, diAAC)
			tempLine = calculateFeatureValueByCorrFactorsDictAndOccurfrequencyType2(corrFactorsDict, occurfrequency, weightFact, lambdaPara, aminoAcid, phyChemList, diAAC)
			g = open(out_file,'a')
			g.write("%s%s"%(sampleType,tempLine))
			g.close()

	f.close()



import re
import sys
import argparse

detectingPythonVersionAndOutputHelpInfo()
typeOfPse, weightFact, lambdaPara, in_file, out_file = argsParser()
detectingTheRationalityOfLambdaPara(in_file, lambdaPara)

if __name__ == '__main__':
	phyChemStandFile = r'C:\Users\liany\Desktop\myPythonScript\featureExtract/standard_value/nine_physicochemical_properties_of_amino_acid_Stand.txt'
	[phyChemDict, aminoAcid, phyChemList] = obtainAminoAcidPhysicoChemicalDict(phyChemStandFile)

	if typeOfPse == 1:
		generateCsvFormatLinebyType1PseAAC(in_file, out_file, weightFact, lambdaPara, phyChemDict, aminoAcid, phyChemList)
	elif typeOfPse == 2:
		generateCsvFormatLinebyType2PseAAC(in_file, out_file, weightFact, lambdaPara, phyChemDict, aminoAcid, phyChemList)
	else:
		printHelpInfo()

	print("------Finished!------")
