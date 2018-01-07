"""
Author : LinDing Group (ZHAO)
Application : file format conversion
Date : 20160902
Usage: Please refer to the README file
Function : Converts the CSV format file to SVM format file!
"""

def generate_svm_file(csv_file, svm_file):
    g = open(svm_file,'w')
    f = open(csv_file).readlines()[1:]

    for eachline in f:
        eachline = eachline.strip().split(',')
        label = eachline[0]
        values = eachline[1:]
        for i in range(len(values)):
            label += '\t%d:%s'%(i+1,values[i])

        g.write('%s\n'%(label))

    g.close()

def argsParser():
	"""参数获取
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-csv",
		type=str,
		default="featureFile.csv",
		help="需转化的CSV文件【输入】"
		)
	args = parser.parse_args()
	return args.csv

def main():
	"""主程序
	"""
	csv_file = argsParser()
	svm_file = os.path.splitext(csv_file)[0]+".svm"
	generate_svm_file(csv_file, svm_file)
	print("文件以生成！：%s"%svm_file)
            
       
import os
import argparse

if __name__ == '__main__':
	main()



