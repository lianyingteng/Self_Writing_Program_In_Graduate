"""程序说明： 对增一法生成的文件进行搜索，找到最大ACC所对应的行，并且以特征数递增的顺序输出到屏幕

	参数：
		-h 打印使用方法，以及所有所需参数
		i 输入文件增一法生成的结果文件【必选参数】
"""

def findOptimalParameterAndPrint(sortedTuple):
	"""查找最优acc对应的特征集，并打印输出
	"""
	maxAcc = -sys.maxsize
	helpDict = dict()

	for fn, tup in sortedTuple:
		if tup[2] < maxAcc: break
		maxAcc = tup[2] if tup[2] > maxAcc else maxAcc
		helpDict[int(re.findall(r'\d+', fn)[0])] = "%s\t%s %s %f"%(fn, tup[0], tup[1], tup[2])

	res = sorted(helpDict.items(), key=lambda asd:asd[0])

	for each in res:
		print(each[1])


def generatePredictValueDict(filename):
	"""文件名作为key，acc作为value。如：dict("out_8.svm" : 82.5)

		返回排序后的元祖 [("out_8.svm", (xx, xx, 82.5), (xx, xx, 82.5)]
	"""
	dict1 = dict()
	f = open(filename)
	for eachline in f:
		temp = eachline.strip().split()
		dict1[temp[0]] = (temp[1], temp[2], float(temp[3]))

	return sorted(dict1.items(), key=lambda asd:asd[1][2], reverse=True)


def argsParser():
	"""参数获取
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"i",
		type=str,
		default="result.txt",
		help="增一法生成的结果文件"
		)
	args = parser.parse_args()
	return args.i


def main():
	"""主程序
	"""
	inputFile = argsParser()
	res = generatePredictValueDict(inputFile)
	findOptimalParameterAndPrint(res)


import re
import sys
import argparse

if __name__ == '__main__':
	main()
