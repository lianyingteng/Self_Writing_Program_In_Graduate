"""通过window版libsvm建模
"""

def argsParser():
	"""参数获取
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"i",
		type=str,
		default="train.svm",
		help="样本训练文件 【输入】"
		)
	parser.add_argument(
		"m",
		type=str,
		default="train.model",
		help="建模文件名 【输出】"
		)
	parser.add_argument(
		"-c",
		type=float,
		default=None,
		help="libsvm最优cost参数 【超参数】"
		)
	parser.add_argument(
		"-g",
		type=float,
		default=None,
		help="libsvm最优gamma参数 【超参数】"
		)
	parser.add_argument(
		"-b",
		type=int,
		default=1,
		help="是否建立概率估计 0-no/1-yes 【超参数】"
		)
	args = parser.parse_args()
	return args.i, args.m, args.c, args.g, args.b


def obtainOptimalParameter(filename):
	"""获取最优的参数组合 cost、gamma

		filename： scale后的训练数据
	"""

	# 运行 grid.py
	os.system(r"python %s -v %d %s > %s_C-G" %(gridPro, n_fold, filename, filename))

	tempLine = open(r'%s_C-G'%(filename)).readlines()[-1]
	cost, gamma, _ = list(
		map(lambda a:float(a), tempLine.split())
		)

	return cost, gamma


def main():
	"""主程序
	"""
	trainSvmF, outModelF, cost, gamma, prob = argsParser()
	# 先对 数据进行 scale
	os.system(r"%s -l 0 -u 1 -s %s.scaleModel %s > %s.scale"%(svmScale, trainSvmF, trainSvmF, trainSvmF))
	
	if cost == None or gamma == None:
		cost, gamma = obtainOptimalParameter("%s.scale"%trainSvmF)

	# 建模
	cmd = "%s -c %f -g %f -b %d %s.scale %s"%(svmTrain, cost, gamma, prob, trainSvmF, outModelF)
	os.system(cmd)

	print("------- model文件已生成！ --------")
	print("scale模型文件： %s.scaleModel"%(trainSvmF))
	print("train模型文件： %s"%(outModelF))



import os
import argparse
if __name__ == '__main__':
	svmPath = r"D:\libsvm-3.22"

	gridPro = svmPath + r"\tools\grid.py"
	svmScale = svmPath + r"\windows\svm-scale.exe"
	svmTrain = svmPath + r"\windows\svm-train.exe"
	n_fold = 5 # 几倍交叉验证

	main()








