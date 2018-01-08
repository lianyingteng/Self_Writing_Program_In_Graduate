def detectExistDirectory(tempDir):
	if os.path.exists(tempDir):
		shutil.rmtree(tempDir)

	os.makedirs(tempDir)


def mergeSampleSequenceFile(posSampleSeqFile, negSampleSeqFile, posLabel, negLabel):
	mergeSampleFile = r"%s%smergeSampleFile.txt"%(os.path.dirname(posSampleSeqFile),os.sep)
	g = open(mergeSampleFile,'w')

	f = open(posSampleSeqFile)
	for eachline in f:
		if eachline[0] == ">": 
			temp = eachline.strip() + "@%d@\n"%posLabel
		else:
			temp = eachline
		g.write(temp)
	f.close()

	f = open(negSampleSeqFile)
	for eachline in f:
		if eachline[0] == ">": 
			temp = eachline.strip() + "@%d@\n"%negLabel
		else:
			temp = eachline
		g.write(temp)
	f.close()
	g.close()

	return mergeSampleFile


def detectingTheRationalityOfLambdaPara(in_file):
	seqLens = []

	f = open(in_file)
	for eachline in f:
		if eachline[0] == ">":
			pass
		else:
			seqLens.append(len(eachline.strip('\n')))

	seqMinLen = min(seqLens)

	print("index = %d"%seqLens.index(seqMinLen))
	
	return seqMinLen


def childProcessing(weiPara, lamPara, tempDir, feaExtProgram):
	os.chdir(tempDir)
	outputFilePre = "output_w%s_r%d"%(weiPara,lamPara)
	os.system(feaExtProgram)
	
	commands = []
	commands.append(r"python3.4 /home/zhaoyaw/myPythonScript/fileFormatConvert/CSVtoSVM.py %s.csv %s.svm"%(outputFilePre, outputFilePre))
	commands.append(r"/home/zhaoyaw/software/libsvm-3.21/svm-scale -l 0 -u 1 %s.svm > %s.svm.scale"%(outputFilePre, outputFilePre))
	commands.append(r"python3.4 /home/zhaoyaw/software/libsvm-3.21/tools/grid.py -v 5 %s.svm.scale > %s_C-G"%(outputFilePre, outputFilePre)) # 5 cross vaild
	for eachCmd in commands:
		os.system(eachCmd)

	f = open(r"../outResult.txt",'a')
	tempLine = open(r'%s_C-G'%(outputFilePre)).readlines()[-1]
	f.write("%s\t%s"%(outputFilePre, tempLine))
	f.close()
	print("	***%s - Finished!***"%outputFilePre)
	os.chdir(os.pardir)




import os,shutil
tempDir = "temp"

posLabel = 1 #正样本标签
negLabel = 0 #负样本标签

#正样本序列文件
posSampleSeqFile = r"/home/zhaoyaw/myProgramming/predictHemolyticActivity/DataSet/PI-2/PI-2pos.fa" 

#负样本序列文件
negSampleSeqFile = r"/home/zhaoyaw/myProgramming/predictHemolyticActivity/DataSet/PI-2/PI-2neg.fa" 

# 特征提取程序
featureExtractProgramDir = r"/home/zhaoyaw/myPythonScript/featureExtract/PseAAC_2type.py"

mergeSampleFile = mergeSampleSequenceFile(posSampleSeqFile, negSampleSeqFile, posLabel, negLabel)
maxLambda = detectingTheRationalityOfLambdaPara(mergeSampleFile)-1 #获得最大Lambda值
if maxLambda >= 30:
	LambdaPara = 30
else:
	LambdaPara = maxLambda
	print("LambdaPara="+str(LambdaPara))

for i in range(1,15):

	wValue = "%.2f"%(0.05*i) # lambda-> [0.05,0.7]
	for j in range(LambdaPara):
		rValue = j+1

		feaExtractFile = "output_w%s_r%d.csv"%(wValue, rValue)
		feaExtProgram = r"python3.4 %s -t 2 -w %s -r %d -i %s -o %s"%(featureExtractProgramDir, wValue, rValue, mergeSampleFile, feaExtractFile)

		detectExistDirectory(tempDir)
		
		childProcessing(wValue, rValue, tempDir, feaExtProgram)


