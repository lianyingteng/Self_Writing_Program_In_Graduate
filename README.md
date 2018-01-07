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


### 2. 特征选择

### 3. 文件格式转化

* [CSVtoSVM.py](https://github.com/lianyingteng/Self_Writing_Program_In_Graduate-/blob/master/CSVtoSVM.py) <br>

**程序说明：** <br>
> `csv文件格式`转化成libsvm可以识别的`svm文件格式` <br>

**参数说明：** <br>
> -h 打印程序所需参数 <br>
> -csv 输入文件，csv格式文件 <br>

**用法实例：**<br>
> `python CSVtoSVM.py -csv featureFile.csv`  注：默认生成 featureFile.svm（输出文件前缀名与输入文件前缀名相同） <br>

* [SVMtoCSV.py](https://github.com/lianyingteng/Self_Writing_Program_In_Graduate-/blob/master/SVMtoCSV.py) <br>

**程序说明：** <br>
> libsvm可以识别的`svm文件格式`转化成`csv文件格式` <br>

**参数说明：** <br>
> -h 打印程序所需参数 <br>
> -svm 输入文件，svm格式文件 <br>
> -num 特征数，来设定将其多少个特征转换成csv文件 <br>

**用法实例：**<br>
> `python SVMtoCSV.py -svm featureFile.svm`  注：默认生成 featureFile.csv（输出文件前缀名与输入文件前缀名相同），也可以通过参数 -num 来设定将其多少个特征转换成csv文件 <br>

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