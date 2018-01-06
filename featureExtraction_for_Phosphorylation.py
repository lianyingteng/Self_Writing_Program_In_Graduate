"""程序说明： 磷酸化工作特征提取程序

	提取的特征包含两部分 1.位点保守性信息； 2.考虑相对位置信息的物化属性，又称特征交叉
	以上两个程序分别对应程序的两个类

	参数：
		-h 打印使用方法，以及所有所需参数
		-i 需输入的蛋白序列样本文件 【注释行的形式 >(1或-1)xxooxxoo】
		-o 需输出的csv格式的特征文件
		-s 需保存的ANOVA的特征排序文件
		--pf 需输入的氨基酸的物化属性文件
"""

class PositionConverationScoringFunction(object):
	"""位点周边残基的保守性得分【不包含位点】 1-30个位点"""
	def __init__(self, sampleFile):
		super(PositionConverationScoringFunction, self).__init__()
		self.sampleFile = sampleFile
		self.p_0 = 0.05
		self.aa = ['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']

	def _getPSFVectorForEachSequence(self, sequence, psf_dict):
		"""获得每条样本序列的psf特征向量表示
		"""
		featureVec = []

		for i in range(len(sequence)):
			if i == 15: continue

			posi = i+1 if i < 15 else i
			featureVec.append(psf_dict[posi][sequence[i]])

		return featureVec


	def __calculateThePositionConservationOfSample(self, count_dict):
		"""计算 样本数据集中 每个位点（1-30）的位点保守型得到 M_l
		"""
		M_l = []

		for posi in range(1, 31):
			m_l = 0
			subDict = count_dict[posi] # 第posi个位点的氨基酸计数字典
			sampleNum = sum(subDict.values()) 
			
			for each_aa in self.aa:
				m_l += ((subDict[each_aa]/sampleNum - self.p_0) ** 2) / self.p_0

			M_l.append(m_l)

		return M_l


	def __statisResidueCountInEachPosition(self, seqSets):
		"""统计得到 每个位点的每种氨基酸的计数， 以字典的形式返回
		"""
		count_dict = dict().fromkeys(list(range(1, len(seqSets[0]))), dict())  # 1 - 30 个位点 （不包含磷酸化位点）
		for each in count_dict: count_dict[each] = dict().fromkeys(self.aa, 0)

		for eachSeq in seqSets:
			for i in range(len(eachSeq)):
				if i == 15: continue
				count_dict[i+1 if i < 15 else i][eachSeq[i]] += 1

		return count_dict

	def _getPositionScoreDictFromTrainSamples(self):
		"""得到 每个位点每种氨基酸 的位置得分函数（psf）的分值，以字典形式返回 并已pickle的形式保存下来（作为webserve的模型）

			psf[位点][氨基酸]
		"""
		pos_samples, neg_samples = [], []

		f = open(self.sampleFile).readlines()
		for i in range(len(f)):
			if f[i][2] == '1':
				pos_samples.append(f[i+1].strip())
			elif f[i][2] == '-':
				neg_samples.append(f[i+1].strip())
			else:
				pass

		pos_count_dict = self.__statisResidueCountInEachPosition(pos_samples)
		neg_count_dict = self.__statisResidueCountInEachPosition(neg_samples)
		M_l_pos = self.__calculateThePositionConservationOfSample(pos_count_dict)
		M_l_neg = self.__calculateThePositionConservationOfSample(neg_count_dict)

		psf_dict = dict().fromkeys(list(range(1, 31)), dict())  # 1 - 30 个位点 （不包含磷酸化位点）
		for each in psf_dict: psf_dict[each] = dict().fromkeys(self.aa, 0)

		pos_sample_size = len(pos_samples)
		for posi in range(1, 31):
			diff = M_l_pos[posi-1] - M_l_neg[posi-1]
			for each_aa in self.aa:
				p_x_l = (pos_count_dict[posi][each_aa] + self.p_0*math.sqrt(pos_sample_size)) / (pos_sample_size + math.sqrt(pos_sample_size))
				psf_dict[posi][each_aa]  = math.log(20 * p_x_l) * diff

		with open(os.path.splitext(self.sampleFile)[0] + '_psf.pkl', 'wb') as f: # 保存
			pickle.dump(psf_dict, f)

		return psf_dict


	def main(self):
		"""得到每条样本序列 对应的 psf特征向量 + 每个特征对应的名称
		"""
		psf_name = list(map(lambda asd: "psf_%d"%asd, range(1,31)))
		pos_score_dict = self._getPositionScoreDictFromTrainSamples()

		pos_scores = []
		f = open(self.sampleFile)
		for eachline in f:
			if eachline[0] != '>':
				pos_scores.append(self._getPSFVectorForEachSequence(eachline.strip(), pos_score_dict))

		return np.array(pos_scores), psf_name


class PositionInformationPlusPhysicochemicalProperty(object):
	"""特征交叉【考虑相对位置的理化属性】"""
	def __init__(self, seqFile, PCPFile):
		super(PositionInformationPlusPhysicochemicalProperty, self).__init__()
		self.seqFile = seqFile
		self.PCPFile = PCPFile # 标准化后的氨基酸物化属性文件


	def _obtainAllFeatureValueCorrLabels(self, windowSize, proName):
		"""得到样本的特征向量对应的标签序列

			label格式： 属性名_lambda_position
		"""
		labels = []

		for eachPro in proName:
			for lbd in range(1, windowSize):
				for pos in range(1, windowSize-lbd+1):
					labels.append("%s_%d_%d"%(eachPro, lbd, pos))

		return labels


	def __getFeatureVectorOfAssignLambda(self, seq, lbd, pro):
		"""得到指定物化性质指定lambda值的属性值
		"""
		featureVal = []
		twins = ["%s%s"%(seq[i], seq[i+lbd]) for i in range(len(seq)) if (i + lbd) < len(seq)]

		for each in twins:
			featureVal.append(pro[each[0]] * pro[each[1]])

		return featureVal


	def _obtainAllFeatureValueForEachSample(self, sampleSeq, proName, proDict):
		"""得到每条样本序列的特征向量
		"""
		featureVec = []

		for eachPro in proName:
			for lbd in range(1, len(sampleSeq)): # lambda 值
				featureVec.extend(self.__getFeatureVectorOfAssignLambda(sampleSeq, lbd, proDict[eachPro]))

		return featureVec

	def _obtainAminoAcidPhysicoChemicalDict(self):
		"""从氨基酸物化属性文件中，获取下列内容：
			1. 所有物化属性名称List
			2. AA、物化属性及其值组成的字典结构 - proDict[物化属性i][氨基酸j]
		"""
		proName, proDict = [], dict()
		f = open(self.PCPFile).readlines()

		for ind in range(len(f)):
			temp = f[ind].strip().split()
			if ind > 0:
				proName.append(temp[0])
				proDict[temp[0]] = dict()
				for i, v in enumerate(temp[1:]): proDict[temp[0]][aaName[i]] = float(v)
			else:
				aaName = temp[1:]

		return proName, proDict

	def main(self):
		"""氨基酸理化属性位置交叉信息
			
			获得所有属性的标签 及 每条样本所有属性的值

			label格式： 属性1_lambda值_position
		"""
		proName, proDict = self._obtainAminoAcidPhysicoChemicalDict()

		sampleLabels = []
		proVals = []

		f = open(self.seqFile)
		for eachline in f:
			if eachline[0] == '>':
				sampleLabels.append('1' if eachline[2] == '1' else '0')
			else:
				sampleSeq = eachline.strip()
				proVals.append(self._obtainAllFeatureValueForEachSample(sampleSeq, proName, proDict))
		f.close()

		proLabels = self._obtainAllFeatureValueCorrLabels(len(sampleSeq), proName)
		return np.array(proVals), proLabels, np.array(sampleLabels)


def argsParser():
	"""参数获取
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-i",
		type=str,
		default="Y_sample.txt",
		help="蛋白序列样本文件 【输入】"
		)
	parser.add_argument(
		"--pf",
		type=str,
		default="nine_physicochemical_properties_of_amino_acid_Stand.txt",
		help="氨基酸物化性质文件"
		)
	parser.add_argument(
		"-o",
		type=str,
		default="Y_feature.csv",
		help="csv格式的特征文件 【输出】"
		)
	parser.add_argument(
		"-s",
		type=str,
		default="Y_sorted_feature.txt",
		help="基于方差的属性排序文件"
		)
	args = parser.parse_args()
	return args.i, args.o, args.pf, args.s

def main():
	"""主程序
	"""
	inSeqFile, outfeaFile, AAproFile, outSortFile = argsParser()

	proVals, proLabels, sampleLabels = PositionInformationPlusPhysicochemicalProperty(inSeqFile, AAproFile).main()
	psfVals, psfLabels = PositionConverationScoringFunction(inSeqFile).main()
	
	proVals = np.hstack((proVals, psfVals))
	proLabels.extend(psfLabels)

	f_score, pVal = f_classif(proVals, sampleLabels)
	anova = dict()
	for a,b in zip(proLabels, zip(f_score, pVal)): anova[a] = b
	anova = sorted(anova.items(), key=lambda asd:asd[1][0], reverse=True)
	
	with open(outSortFile, 'w') as osf: # 生成特征排序文件
		osf.write("feature-name\tF-score\tP-value\n")
		for each in anova: osf.write("%s\t%.6f\t%.6f\n"%(each[0], each[1][0], each[1][1]))

	sortedFeatureLabel = []
	for i, each in enumerate(anova): # 获得排序后的特征向量
		#if each[1][0] <= 1: break  ### 控制方差F-score的最小值【注释-表示不筛选】
		sortedFeatureLabel.append(each[0])
		proval_vec = proVals[:, proLabels.index(each[0])][:, np.newaxis]
		proval_vecs =  proval_vec if i == 0 else np.hstack((proval_vecs, proval_vec)) # 排序后特征向量 

	with open(outfeaFile, 'w') as off: # 生成排好序的特征文件
		off.write('class,%s\n'%(','.join(sortedFeatureLabel)))
		for i in range(len(sampleLabels)):
			off.write(
				str(sampleLabels[i]) + ',%s\n'%(
					','.join(
						list(map(
							lambda asd:"%.6f"%asd, proval_vecs[i])
						)
						)
					)
				)



import os
import math
import argparse
import itertools
import sklearn
import pickle
import numpy as np
from sklearn.feature_selection import f_classif

if __name__ == '__main__':
	main()
	print("Finished!")
	