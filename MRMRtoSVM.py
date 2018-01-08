def printHelpInfo():
	print("""
Useful: 
		
	python mrmrToSVN.py inputFilename1_Sorted  inputFilename2_CSV

  parameter description:

	* inputFilename1_Sorted - The file contains "mRMR features"

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

def obatinMrmrSortedFeatureNamesList(mrmrSortedFile):
	featureNames = []
	judge = False

	f= open(mrmrSortedFile)
	for eachline in f:
		if "mRMR features" in eachline:
			judge = True
			continue
		if judge == True:
			if eachline == "\n":
				break
			if not eachline[0].isdigit():
				continue
			featureNames.append(eachline.split("\t")[2].strip(" "))

	return featureNames

def generateSvmFileOfSortedFeatures(inCsvFile, mrmrSortedFile):
	outputFilename = os.path.splitext(inCsvFile)[0] + "_MrmrSorted.svm"
	sortedFeatureList = obatinMrmrSortedFeatureNamesList(mrmrSortedFile)
	
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
mrmrSortedFile = sys.argv[1]
inCsvFile = sys.argv[2]
#mrmrSortedFile = "output_w0.7r22.csv.mrmr"
#inCsvFile = "output_w0.7r22.csv"
if __name__ == '__main__':
	generateSvmFileOfSortedFeatures(inCsvFile, mrmrSortedFile)
