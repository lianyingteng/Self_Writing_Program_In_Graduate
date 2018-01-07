# 研究生阶段科研方面自写程序【生信】
---
`注： 以下所有程序编写时都是基于python3版本， 所以当你使用时均需使用python3版本去执行`

### 特征提取

* [featureExtraction_for_Phosphorylation.py](https://github.com/lianyingteng/Self_Writing_Program_In_Graduate-/blob/master/featureExtraction_for_Phosphorylation.py) <br>

**程序说明：**<br>
> 磷酸化工作特征提取程序。 提取的特征包含两部分: <br>
> (1) 位点附近残基的位点保守性信息 <br>
> (2) 位点附近残基的物化属性关联信息 <br>

**参数说明：** <br>
> -h 打印使用方法，以及所有所需参数 <br>
> -i 需输入的蛋白序列样本文件 【注释行的形式 `>(1或-1)xxooxxoo】` <br>
> -o 需输出的csv格式的特征文件 <br>
> -s 需保存的ANOVA的特征排序文件 <br>
> --pf 需输入的氨基酸的物化属性文件 <br>

**用法实例：**<br>
> python featureExtraction_for_Phosphorylation.py -i Y_sample.txt -o Y_feature.csv -s Y_sorted_feature.txt --pf physicochemical_properties.txt <br>


### 特征选择

### 文件格式转化

### 择优与调试

* [runSvmFindBestFeatureSet.py](https://github.com/lianyingteng/Self_Writing_Program_In_Graduate-/blob/master/runSvmFindBestFeatureSet.py) <br>

**程序说明：** <br>
> 增一法运行svm，得到最优特征集（多线程程序） <br>

**参数说明：** <br>
> -h 打印程序所需参数 <br>
> -i 输入文件，svm格式，特征是经过贡献性大小排序的 <br>
> --cpuNum 程序使用的线程数【默认4】 <br>

**用法实例：**<br>
> python runSvmFindBestFeatureSet.py -i featureFile.svm --cpuNum 4 <br>