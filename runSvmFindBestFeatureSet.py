"""程序说明： 增一法运行svm，得到最优特征集

	参数：
		-h 打印程序所需参数
		-i 输入文件，svm格式，特征是经过贡献性大小排序的
		--cpuNum 程序使用的线程数【默认4】
"""

def removeFile(startFilename):
	fileList = os.listdir(os.curdir)
	for eachFile in fileList:
		if re.search(r'^%s'%startFilename, eachFile) == None:
			pass
		else:
			os.remove(eachFile)


def generateIterativeFeatureFile(numbers, inputFilename):
	outFileName = "out_%d.svm"%(numbers)

	g = open(outFileName,'w')
	f = open(inputFilename)
	for eachline in f:
		strings = ''
		temp = eachline.strip().split("\t")
		for i in range(numbers+1):
			strings += "\t%s"%temp[i]
		g.write(strings.strip("\t") + "\n")
	
	f.close()
	g.close()

	return outFileName


def childProcessing(numbers, inputFilename, outResult):
	startFilename = generateIterativeFeatureFile(numbers, inputFilename)

	commands = []
	commands.append(r"/home/ywzhao/software/libsvm-3.22/svm-scale -l 0 -u 1 %s > %s.scale"%(startFilename, startFilename))
	commands.append(r"python3.5 /home/ywzhao/software/libsvm-3.22/tools/grid.py -v 5 %s.scale > %s_C-G"%(startFilename, startFilename)) # 5 cross vaild

	for eachCmd in commands:
		os.system(eachCmd)

	f = open(outResult,'a')
	tempLine = open(r'%s_C-G'%(startFilename)).readlines()[-1]
	f.write("%s\t%s"%(startFilename, tempLine))
	f.close()
	print("	***%s - Finished!***"%startFilename)

	removeFile(startFilename)


def obtainFileMaxFeatureNumber(inputFilename):
	maxNum = 0
	f = open(inputFilename)
	for eachline in f:
		length = len(eachline.split("\t")) - 1
		maxNum = max(maxNum, length)
	return maxNum

def mainProcessing(inputFilename, tempDirect, cpuNum, outResFile):
	os.chdir(tempDirect)
	maxFeatureNum = obtainFileMaxFeatureNumber(inputFilename)
	featureNumList = list(range(1,maxFeatureNum+1))
	
	num = 0
	threads = []
	for fInde in range(len(featureNumList)):
		featureNum = featureNumList[fInde]
		num += 1

		t = threading.Thread(target=childProcessing, args=(featureNum, inputFilename, outResFile))
		threads.append(t)

		if (num == cpuNum) or (featureNum == maxFeatureNum):
			for t in threads:
				t.start()
			for t in threads:
				t.join()

			num = 0
			threads = []
		else:
			pass

	os.chdir(os.pardir)


def detectExistDirectory(tempDir):
	if os.path.exists(tempDir):
		shutil.rmtree(tempDir)

	os.makedirs(tempDir)

def argsParser():
	"""参数获取
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-i",
		type=str,
		default="featureFile.svm",
		help="需要执行增益法的特征文件"
		)
	parser.add_argument(
		"--cpuNum",
		type=int,
		default=4,
		help="多线程数"
		)
	args = parser.parse_args()
	args.cpuNum = 4 if args.cpuNum > 8 else args.cpuNum
	return args.i, args.cpuNum

def main():
	"""主程序
	"""
	inSvmFeaFile, cpuNum = argsParser()
	pathPrefix = os.getcwd() + os.path.sep
	tempDir = pathPrefix + "temp"
	outResFile = pathPrefix + os.path.splitext(inSvmFeaFile)[0] + "_result.txt"
	inSvmFeaFile = pathPrefix + inSvmFeaFile

	detectExistDirectory(tempDir)
	mainProcessing(inSvmFeaFile, tempDir, cpuNum, outResFile)


import os
import re
import sys
import shutil
import argparse
import threading

if __name__ == '__main__':
	main()