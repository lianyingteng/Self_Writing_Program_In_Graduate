"""
Author : LinDing Group (ZHAO)
Application : feature selection
Date : 20161123
Usage: Please refer to the README file
Intro : This is a feature selection technique based on binomial distribution!
"""
def detecting_python_version_AND_output_help_info():

    if sys.version[0] == '2':
        print("""\nVersionError: The current python version: '%s',
    You must use python version 3 or later to run this script!\n"""%((sys.version).split('\n')[0]))
        exit(0)
    else:
        pass

    try:
        if sys.argv[1] == "--help":
            print_help_info()
        else:
            pass
    except:
        print_help_info()


def detecting_parameter():
    featureRank_file = 'sortedRank.file'
    chooseMethod = 'MaxC'
    judge = False

    argv_count = len(sys.argv)
    argv_list = list(sys.argv)
    index_list = list(range(1, argv_count))

    if (argv_count%2) != 0: # 参数总数是奇数
        if '-m' in argv_list:
            m_index = argv_list.index('-m')
            if argv_list[m_index+1] in ['MaxC','MinI']:
                chooseMethod = argv_list[m_index+1]
            else:
                print("\nParameter Error!")
                print_help_info()
            del index_list[index_list.index(m_index)]; del index_list[index_list.index(m_index+1)]
            
        if '-s' in argv_list:
            s_index = argv_list.index('-s')
            featureRank_file = argv_list[s_index+1]
            del index_list[index_list.index(s_index)]; del index_list[index_list.index(s_index+1)]

        in_filenameList_file = argv_list[index_list[0]]
        ou_sortedFeature_file = argv_list[index_list[-1]]
        judge = True
    
    if judge == False:
        print("\nParameter Error!")
        print_help_info()

    return chooseMethod, featureRank_file, in_filenameList_file, ou_sortedFeature_file


def print_help_info():
    print("""
    Usage: python BinomialDistribution.py [-m MaxC/MinI] [-s sortedRank.file] input_filenameList.txt output_sortedFeature.csv
    
    Other details, please read the README file!
""")
    exit(0)


def operation_main(chooseMethod, featureRank_file, in_filenameList_file, ou_sortedFeature_file):
    unsorted_featureCsv_file = 'unsorted_feature.csv'
    triptide_list = get_all_tripeptide(unsorted_featureCsv_file)
    ClvalueDict = get_eachTypeProteinSeq_ClDict(in_filenameList_file, triptide_list, unsorted_featureCsv_file)
    # 选择合适的特征排序策略
    if chooseMethod == 'MaxC':
        sortedFeature_by_maxClvalue(ClvalueDict, triptide_list, featureRank_file)
    else:
        sortedFeature_by_indexOfEachType(ClvalueDict, triptide_list, featureRank_file)
    # 生成排序后的csv文件
    generate_sortedFeatureCsvFile(triptide_list, unsorted_featureCsv_file, featureRank_file, ou_sortedFeature_file)


# 生成8000三肽列表  
def get_all_tripeptide(filename):
    ou_oriFeature_svm = open(filename,'w') #生成还未排序特征的csv特征文件 - 特征名字行
    
    str1 = 'class'
    aa = ['A','C','D','E','F','G','H','I','K','L',
          'M','N','P','Q','R','S','T','V','W','Y']
    triptide_list = []
    for i in aa:
        for j in aa:
            for k in aa:
                tripeptide = i + j + k
                triptide_list.append(tripeptide)
                str1 += ',%s'%(tripeptide)

    ou_oriFeature_svm.write(str1+'\n')
    ou_oriFeature_svm.close()
                
    return triptide_list


# 得到一个CL值的字典，包含每一类样本的8000个三肽的CL值
def get_eachTypeProteinSeq_ClDict(in_filenameList_file, triptide_list, unsorted_feature_csv):
    [pri_pro, tri_num_type, tri_num_all, typeLabels] = getAllVariableValue_inProteinSequence(in_filenameList_file, triptide_list, unsorted_feature_csv)

    ClValueDict = dict()
    for eachTypeLabel in typeLabels:
        ClValueDict[eachTypeLabel] = dict()
        qj = pri_pro[eachTypeLabel]
        for eachTripeName in triptide_list:
            Ni = tri_num_all[eachTripeName]
            nij = tri_num_type[eachTypeLabel][eachTripeName]

            ClValueDict[eachTypeLabel][eachTripeName] = binomailDistributionFunction_returnCL(nij, Ni,qj)
    return ClValueDict


def getAllVariableValue_inProteinSequence(in_filenameList_file, triptide_list, filename):
    proteinSeq_filename = obtain_proteinSeq_filenameList(in_filenameList_file)
    class_num = len(proteinSeq_filename)

    tri_num_type = dict()
    typeLabels = []
    for i in range(class_num):
        typeLabel = str(i+1)
        typeLabels.append(typeLabel)
        eachname = proteinSeq_filename[i]
        tri_num_type[typeLabel] = obtainAllVariableValue_inEachTypeProteinSequence(eachname, typeLabel, triptide_list, filename)
    tri_num_all = obtain_tripetide_allNumber(tri_num_type, triptide_list, typeLabels)
    
    database_totalTriPeNum = sum(tri_num_all.values())
    pri_pro = obtain_eachType_priorProbability(tri_num_type, database_totalTriPeNum, typeLabels)

    return pri_pro, tri_num_type, tri_num_all, typeLabels


def obtain_proteinSeq_filenameList(in_filenameList_file):
    proteinSeq_filename = []
    
    f = open(r'%s'%(in_filenameList_file))
    for eachline in f:
        if eachline != '\n':
            proteinSeq_filename.append(eachline.strip('\n'))
    f.close()
    return proteinSeq_filename


def obtainAllVariableValue_inEachTypeProteinSequence(proSeqFname, typeLabel, triptideList, filename):
    ou_oriFeature_svm = open(filename,'a') #生成还未排序特征的csv特征文件
    
    each_typeSeq_c = dict()
    each_typeSeq_c = each_typeSeq_c.fromkeys(triptideList,0)
    
    f = open(r'%s'%(proSeqFname))
    for each in f:
        if each[0] not in ['>','\n']:
            sequence = each.strip('\n')
            
            each_seq_c = dict()
            each_seq_c = each_seq_c.fromkeys(triptideList,0)
            
            length = len(sequence)
            for i in range(length-2):
                triPe = sequence[i:i+3]
                each_seq_c[triPe] += 1
                each_typeSeq_c[triPe] += 1

            ou_oriFeature_svm.write(gain_sample_svmLine(each_seq_c, typeLabel, triptideList))

    f.close()
    ou_oriFeature_svm.close()

    return each_typeSeq_c


def gain_sample_svmLine(each_seq_c, typeLabel, triptideList):
    svmLine = typeLabel
    
    total_count = sum(each_seq_c.values())
    for eachTriPe in triptideList:
        triPe_value = each_seq_c[eachTriPe]
        if triPe_value == 0:
            svmLine += ',0'
        else:
            svmLine += ',%.6f'%(triPe_value/total_count)

    return svmLine+'\n'


def obtain_tripetide_allNumber(tri_num_type, triptide_list, typeLabels):
    tri_num_all = dict()

    for eachTriPe in triptide_list:
        tri_num_all[eachTriPe] = sum([tri_num_type[eachTypeLabel][eachTriPe] for eachTypeLabel in typeLabels])

    return tri_num_all


def obtain_eachType_priorProbability(tri_num_type, database_totalTriPeNum, typeLabels):
    pri_pro = dict()

    for eachTypeLabel in typeLabels:
        pri_pro[eachTypeLabel] = sum(tri_num_type[eachTypeLabel].values())/database_totalTriPeNum

    return pri_pro


# 二项分布主要函数体
def binomailDistributionFunction_returnCL(nij, Ni,qj):
    prob = 0

    for m in range(nij, Ni+1):
        prob += _mainFormula(m, Ni, qj)

    CLij = 1 - prob

    return CLij


def _mainFormula(m, Ni, qj):
    temp = Ni-m
    if Ni != 0:
        if m < temp:
            _nume = range(temp+1, Ni+1) # numerator[分子]
            _deno = range(1, m+1) # denominator[分母]
            _grou = zip(_nume, _deno)

            resu = 1
            for (i,j) in _grou:
                resu *= ((i/j) * qj)
            resu = resu * ((1-qj) ** temp)
            
        else:
            _nume = range(m+1, Ni+1) # numerator[分子]
            _deno = range(1, temp+1) # denominator[分母]
            _grou = zip(_nume, _deno)

            resu = 1
            for (i,j) in _grou:
                resu *= ((i/j) * (1-qj))
            resu = resu * (qj ** m)
            
    else:
        return 1

    return resu


# MaxC - 基于最大CL值的排序策略
def sortedFeature_by_maxClvalue(ClvalueDict, triptide_list, featureRank_file):
    typeLabels = sorted(ClvalueDict.keys())
    max_ClvalueDict = get_eachTripetideMaxClValueDict_fromClvalueDict(ClvalueDict, triptide_list, typeLabels)
    max_ClvalueDict_valueList = list(max_ClvalueDict.values()) # 方便添加add_order项
    
    sorted_result = sorted(max_ClvalueDict.items(), key=lambda asd:asd[1], reverse=True)
    
    note_head = 'Rank\tFeature'
    for eachTyLa in typeLabels:
        note_head += '\ttype_%s_CL'%eachTyLa
    
    feaRank_f = open(r'%s'%featureRank_file, 'w')
    feaRank_f.write('There is a %d classification problem!\n\tUse the strategy: MaxC\n\n\n'%len(typeLabels))
    feaRank_f.write('-'*8 + 'MaxC Sorted Feature Set' + '-'*8 + '\n')
    feaRank_f.write('%smax_CL\tadd_order\n'%note_head)
    orderLabel = 1
    temp = max(max_ClvalueDict_valueList)
    for i in range(len(sorted_result)):
        [tripeTide, maxClvalue] = sorted_result[i]
        
        stay_wirte_str = '%d\t%s'%((i+1),tripeTide)
        for eachTyLa in typeLabels:
            stay_wirte_str += '\t%f'%(ClvalueDict[eachTyLa][tripeTide])
        if temp == maxClvalue:
            pass
        else:
            temp = maxClvalue
            orderLabel = orderLabel + 1
        stay_wirte_str += '\t%f\t%d\n'%(maxClvalue,(orderLabel))
        
        feaRank_f.write(stay_wirte_str)
        
    feaRank_f.close()
    
    
def get_eachTripetideMaxClValueDict_fromClvalueDict(ClvalueDict, triptide_list, typeLabels):
    max_ClvalueDict = dict()
    for eachtri in triptide_list:
        eachTripetideClvalue = []
        for eachTypeLabel in typeLabels:
            eachTripetideClvalue.append(ClvalueDict[eachTypeLabel][eachtri])
        
        max_ClvalueDict[eachtri] = max(eachTripetideClvalue)

    return max_ClvalueDict


# MinI - 基于最小索引的排序策略
def sortedFeature_by_indexOfEachType(ClvalueDict, triptide_list, featureRank_file):
    typeLabels = sorted(ClvalueDict.keys())
    featureRankTuple = get_featureRankDict_inClvalueTuple(ClvalueDict,triptide_list,typeLabels)

    feaRank_f = open(r'%s'%featureRank_file, 'w')
    feaRank_f.write('There is a %d classification problem!\n\tUse the strategy: MinI\n\n\n'%len(typeLabels))
    feaRank_f.write('-'*8 + 'MinI Sorted Feature Set' + '-'*8 + '\n')
    feaRank_f.write('Rank\tFeature\tadd_order\n')

    rank_num = 0
    for (tripe, rank) in featureRankTuple:
        rank_num += 1
        feaRank_f.write('%d\t%s\t%d\n'%(rank_num, tripe, rank))

    feaRank_f.close()


def get_featureRankDict_inClvalueTuple(ClvalueDict,triptide_list,typeLabels):
    featureRankDict = dict()
    temp = dict() # 存放每类特征排序后的元组

    for eachTyLa in typeLabels:
        type_ClvalueDict = ClvalueDict[eachTyLa]
        sorted_result = sorted(type_ClvalueDict.items(), key=lambda asd:asd[1], reverse=True)
        tripetides = []
        for (tripetide,Cls) in sorted_result:
            tripetides.append(tripetide)
        temp[eachTyLa] = tripetides

    for eachTripe in triptide_list:
        rank_list = []
        for eachTyLa in typeLabels:
            rank_list.append((temp[eachTyLa].index(eachTripe)+1))
        featureRankDict[eachTripe] = min(rank_list)

    featureRankTuple = sorted(featureRankDict.items(), key=lambda asd:asd[1], reverse=False)

    return featureRankTuple


# 生成排序后的csv文件
def generate_sortedFeatureCsvFile(triptide_list, unsorted_featureCsv, featureRank, ou_sortedFeature):
    rela_pos_list = get_relativePositionOfSortedFeatureSet_InTriptideList(featureRank, triptide_list)

    f = open(unsorted_featureCsv)
    g = open(ou_sortedFeature,'w')
    for eachline in f:
        if eachline != '\n':
            line_split = eachline.strip().split(',')
            stay_write_str = line_split[0]
            for eachindex in rela_pos_list:
                stay_write_str += ',%s'%(line_split[eachindex])
            g.write(stay_write_str+'\n')
        
    f.close()
    g.close()
    

def get_relativePositionOfSortedFeatureSet_InTriptideList(featureRank, triptide_list):
    rela_pos_info = []
    
    sortedFeatureSet = obtain_sortedFeatureSet_from_featureRankFile(featureRank)
    for each in sortedFeatureSet:
        rela_pos_info.append((triptide_list.index(each)+1)) # 索引+1

    return rela_pos_info
    

def obtain_sortedFeatureSet_from_featureRankFile(featureRank):
    sortedFeatureSet = []
    
    f = open(featureRank)
    for eachline in f:
        if eachline[0].isdigit():
            sortedFeatureSet.append(eachline.split()[1])
        else:
            pass
        
    return sortedFeatureSet


import sys

detecting_python_version_AND_output_help_info()
[chooseMethod, featureRank, in_filenameList, ou_sortedFeature] = detecting_parameter()

if __name__ == '__main__':
    operation_main(chooseMethod, featureRank, in_filenameList, ou_sortedFeature)
    
