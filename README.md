# 科研方面自写程序【生信】
---
`注： 以下所有程序编写时都是基于python3版本， 所以当你使用时均需使用python3版本去执行`

### 1. 特征提取

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
> `python featureExtraction_for_Phosphorylation.py -i Y_sample.txt -o Y_feature.csv -s Y_sorted_feature.txt --pf physicochemical_properties.txt` <br>

* ***~~psekncRna_2type.py~~*** <br>

**程序说明：** <br>
> 基于RNA的2型PseKnc <br>

**参数说明：** <br>
> -t  设定PseKNC的类型<br>
>> 1 -> Type 1 PseKNC 【这个程序没有写】 <br>
>> 2 -> Type 2 PseKNC.【只有这个程序】 <br>

> -w 伪组分的权重参数，通常设定范围0.1到1 【默认0.5】 <br>
> -r 位置关联参数 <br>
> -i 需输入的fasta格式序列文件 <br>
> -o 输出的csv格式的特征文件 <br>

**用法实例：**<br>
> `python psekncRna_2type.py -t 2 -w 0.05 -r 100 -i inputFilename -o outputFilename`  <br>

* ***~~PseAAC_2type.py~~*** <br>

**程序说明：** <br>
> 基于蛋白序列的2型PseAAC（20个氨基酸频率 + 9\*lambda个伪组分） <br>

**参数说明：** <br>
> -t  设定PseAAC的类型<br>
>> 1 -> Type 1 PseAAC 【这个程序没有写】 <br>
>> 2 -> Type 2 PseAAC.【只有这个程序】 <br>

> -w 伪组分的权重参数，通常设定范围0.1到1 【默认0.5】 <br>
> -r 位置关联参数 <br>
> -i 需输入的fasta格式序列文件 <br>
> -o 输出的csv格式的特征文件 <br>

**用法实例：**<br>
> `python3.4 PseAAC_2type.py -t 2 -w 0.05 -r 100 -i inputFilename -o outputFilename`  <br>

* ***~~PseAAC_2type_diAAC.py~~*** <br>

**程序说明：** <br>
> 基于蛋白序列的2型PseAAC（400个二肽频率 + 9\*lambda个伪组分） <br>

**参数说明：** <br>
> -t  设定PseAAC的类型<br>
>> 1 -> Type 1 PseAAC 【这个程序没有写】 <br>
>> 2 -> Type 2 PseAAC.【只有这个程序】 <br>

> -w 伪组分的权重参数，通常设定范围0.1到1 【默认0.5】 <br>
> -r 位置关联参数 <br>
> -i 需输入的fasta格式序列文件 <br>
> -o 输出的csv格式的特征文件 <br>

**用法实例：**<br>
> `python3.4 PseAAC_2type_diAAC.py -t 2 -w 0.05 -r 100 -i inputFilename -o outputFilename`  <br>


### 2. 特征选择

* ***~~ANOVA.py~~*** <br>

**程序说明：** <br>
> 使用方差分析思想对输入特征进行共线性大小排序（支持多分类） <br>

**参数说明：** <br>
> -i 输入文件，csv格式文件 <br>
> -o 输出文件，特征排序后的结果文件 <br>

**用法实例：**<br>
> `python ANOVA.py -i test.csv -o result.anova`  <br>

**算法参考** <br>
> `[1] Lin, H. et al. Predicting cancerlectins by the optimal g-gap dipeptides. Scientific reports 5, doi:10.1038/srep16964 (2015)` <br>

* ***~~BinomialDistribution.py~~*** <br>

**程序说明：** <br>
> 本程序基于二项分布对8000种三肽的特征进行特征选择（支持多分类） <br>

**参数说明：** <br>
> 可选参数： <br>
>> -m MaxC/MinI  
>>> MaxC表示根据每个三肽在各类中的最大CLs值进行排序[默认] <br>
>>> MinI表示依据三肽在各类中的最小排序索引值进行排序 <br>

>> -s sortedRank.file  sortedRank.file是排序结果的输出文件名 <br>

> 必选参数： <br>
>> pathOfFasta.txt  样本蛋白fasta序列文件的文件名【包含路径】，详见test目录下的相应文件【myPythonScript】 <br>
>> feature.csv  排序后的特征文件【csv格式】 <br>

**用法实例：**<br>
> `python BinomialDistribution.py [-m MaxC/MinI][-s sortedRank.file] pathOfFasta.txt feature.csv`  <br>

**算法参考** <br>
> `[1] Zhu, P. P. et al. Predicting the subcellular localization of mycobacterial proteins by incorporating the optimal tripeptides into the general form of pseudo amino acid composition. Molecular bioSystems 11, 558-563, doi:10.1039/c4mb00645c (2015)` <br>

### 3. 文件格式转化

* [CSVtoSVM.py](https://github.com/lianyingteng/Self_Writing_Program_In_Graduate-/blob/master/CSVtoSVM.py) <br>

**程序说明：** <br>
> `csv文件格式`转化成libsvm可以识别的`svm文件格式` <br>

**参数说明：** <br>
> -h 打印程序所需参数 <br>
> -csv 输入文件，csv格式文件 <br>

**用法实例：**<br>
> `python CSVtoSVM.py -csv featureFile.csv`  注：默认生成 featureFile.svm（输出文件前缀名与输入文件前缀名相同） <br>

* ***~~SVMtoCSV.py~~*** <br>

**程序说明：** <br>
> libsvm可以识别的`svm文件格式`转化成`csv文件格式` <br>

**参数说明：** <br>
> -h 打印程序所需参数 <br>
> -svm 输入文件，svm格式文件 <br>
> -num 特征数，来设定将其多少个特征转换成csv文件 <br>

**用法实例：**<br>
> `python SVMtoCSV.py -svm featureFile.svm`  注：默认生成 featureFile.csv（输出文件前缀名与输入文件前缀名相同），也可以通过参数 -num 来设定将其多少个特征转换成csv文件 <br>

* ***~~ANOVAtoSVM.py~~*** <br>

**程序说明：** <br>
> 将ANOVA的排序结果转化成SVM文件 <br>

**参数说明：** <br>
> 两个必选参数： 
>> 程序（ANOVA.py）输出的特征排序文件，对应于用法实例中的result.anova
>> 程序（ANOVA.py）输入的csv文件，对应于用法实例中的test.csv

**用法实例：**<br>
> `python ANOVAtoSVN.py result.anova  test.csv` <br>

* ***~~MRMRtoSVM.py~~*** <br>

**程序说明：** <br>
> 将mRMR的排序结果转化成SVM文件 <br>

**参数说明：** <br>
> 两个必选参数： 
>> 程序（MRMR）输出的特征排序文件，对应于用法实例中的result.mrmr
>> 程序（MRMR）输入的csv文件，对应于用法实例中的test.csv

**用法实例：**<br>
> `python MRMRtoSVM.py result.mrmr  test.csv` <br>

### 4. 择优与调试

* [runSvmFindBestFeatureSet.py](https://github.com/lianyingteng/Self_Writing_Program_In_Graduate-/blob/master/runSvmFindBestFeatureSet.py) <br>

**程序说明：** <br>
> 增一法运行svm，得到最优特征集（多线程程序） <br>

**参数说明：** <br>
> -h 打印程序所需参数 <br>
> -i 输入文件，svm格式，特征是经过贡献性大小排序的 <br>
> --cpuNum 程序使用的线程数【默认4】 <br>

**用法实例：**<br>
> `python runSvmFindBestFeatureSet.py -i featureFile.svm --cpuNum 4`   注：线程数最好是4，最大不能超过8，避免影响其他同学使用 <br>

* [findOptimalParameter.py](https://github.com/lianyingteng/Self_Writing_Program_In_Graduate-/blob/master/findOptimalParameter.py) <br>

**程序说明：** <br>
> 对增一法生成的文件进行搜索，找到最大ACC所对应的行，并且以特征数升序的形式输出到屏幕 <br>

**参数说明：** <br>
> -h 打印使用方法，以及所有所需参数 <br>
> i 输入文件增一法生成的结果文件【必选参数】 <br>

**用法实例：**<br>
> `python findOptimalParameter.py S_feature_result.txt`   注：该文件（S_feature_result.txt）是程序（runSvmFindBestFeatureSet.py）的产出<br>