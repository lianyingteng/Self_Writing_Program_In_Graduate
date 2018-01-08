def printHelpInfo():
	print("""
Useful: 
		
	python ANOVAtoSVN.py inputFilename1_Sorted  inputFilename2_CSV

  parameter description:

	* inputFilename1_Sorted - The file contains "ANONA Sorted Feature Set"

	* inputFilename2_CSV - The standard CSV file
	
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

def obatinANOVASortedFeatureNamesList(anovaSortedFile):
	featureNames = []
	f = open(anovaSortedFile)
	for eachline in f:
		feaName = re.findall(r"^\d+\s(.+)\s\d", eachline)
		if feaName == []:
			pass
		else:
			featureNames.append(feaName[0])
	f.close()
	
	return featureNames

def generateSvmFileOfSortedFeatures(inCsvFile, anovaSortedFile):
	outputFilename = os.path.splitext(inCsvFile)[0] + "_AnovaSorted.svm"
	sortedFeatureList = obatinANOVASortedFeatureNamesList(anovaSortedFile)
	g = open(outputFilename, 'w')
	
	f = open(inCsvFile)
	countLine = 0
	for eachline in f:
		countLine += 1
		temp = eachline.strip().split(",")
		if countLine == 1:
			featureNames = temp[1:]
			continue

		outStr = "%s"%temp[0]
		valueNames = temp[1:]

		countNum = 0
		for eachFea in sortedFeatureList:
			countNum += 1
			feaValue = valueNames[featureNames.index(eachFea)]
			outStr += '\t%d:%s'%(countNum, feaValue)
		g.write(outStr + '\n')

	f.close()
	g.close()

	print("\n---Finished!---\nThe results are stored in a file: %s"%outputFilename)





import re
import os
import sys

detectingPythonVersionAndOutputHelpInfo()
anovaSortedFile = sys.argv[1]
inCsvFile = sys.argv[2]

if __name__ == '__main__':
	generateSvmFileOfSortedFeatures(inCsvFile, anovaSortedFile)



