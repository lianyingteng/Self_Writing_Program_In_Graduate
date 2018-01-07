"""
Author : LinDing Group (ZHAO)
Application : file format conversion
Date : 20160901
Usage: Please refer to the README file
Function : Converts the SVM format file to CSV format file!
""" 
def get_nullValue_value_line(value_line,start,end):
    nullValue_line = ',0' * (end-start) 
    value_line = value_line + nullValue_line
    return value_line
    

def get_csv_value_line(temp, feature_num):
    value_line = ''

    count = 0
    for each in temp:
        count += 1
        [label,value] = each.split(':')
        label = int(label)

        if count == label:
            pass
        elif count < label:
            value_line = get_nullValue_value_line(value_line,count,label)
            count = label
        else:
            print('Note: There are some errors!')
            assert 0
            
        value_line += ',%s'%(value)

    if count < feature_num:
        value_line = value_line + ',0'*(feature_num-count)

    value_line = value_line.strip(',')
    
    return value_line


def get_note_line(feature_num):
    """得到CSV文件的第一行：注释行
    """
    note_line = 'class'

    for i in range(feature_num):
        note_line += ',f_%d'%(i+1)
    note_line = note_line + '\n'

    return note_line

def generate_csv_file(svm_file, csv_file, feature_num):
    """转换并创建CSV文件
    """
    g = open(csv_file,'w')
    g.write(get_note_line(feature_num))

    f = open(svm_file)
    for eachline in f:
        eachline = eachline.strip().split()
        label = eachline[0]
        value = get_csv_value_line(eachline[1:], feature_num)

        g.write('%s,%s\n'%(label, value))

    f.close()
    g.close()



def getMaxFeatureNumber(svm_file):
    """得到SVM文件中所有特征的数量（共多少特征）
    """
    fNum = 0
    
    f = open(svm_file)
    for eachline in f:
        final_set = eachline.split()[-1]
        maxFeaNum = int(final_set.split(':')[0])
        fNum = max(fNum, maxFeaNum)   

    f.close()

    return fNum    


def argsParser():
    """参数获取
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-svm",
        type=str,
        default="featureFile.svm",
        help="需转化的SVM文件【输入】"
        )
    parser.add_argument(
        "-num",
        type=int,
        default=None,
        help="将前多少特征转换成CSV格式文件？【默认：全部】"
        )

    args = parser.parse_args()
    return args.svm, args.num
 

def main():
    """主程序
    """
    svm_file, feature_num = argsParser()
    csv_file = os.path.splitext(csv_file)[0]+".csv"

    feature_num = getMaxFeatureNumber(svm_file) if feature_num == None else feature_num
    generate_csv_file(svm_file, csv_file, feature_num)

    print("文件以生成！：%s"%csv_file)
            
       
import os
import argparse

if __name__ == '__main__':
    main()