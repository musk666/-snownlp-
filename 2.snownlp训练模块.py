from snownlp import sentiment
from lxml import etree
from snownlp import SnowNLP
import pandas as pd
import xlwt

# 二、SnowNLP分类训练函数
def SnowNLP_TRAIN(TrainPath):
    # 0.指定训练模型的保持路径
    pospath = "D:\\Users\\Musk18\\Desktop\\数据挖掘课设\\pos.txt"
    negpath = "D:\\Users\\Musk18\\Desktop\\数据挖掘课设\\neg.txt"
    sentimentpath = "F:/ProgramData/Anaconda3/envs/untitled2/Lib/site-packages/snownlp/sentiment/sentiment.marshal"
    # 1.将爬取的影评按照打分，分为正负样本，并分别保存，正样本保存到pos.txt，负样本保存到neg.txt
    posfile = open(pospath, 'w', encoding='utf-8')
    negfile = open(negpath, 'w', encoding='utf-8')
    df = pd.read_excel(TrainPath + '评分和影评.xls')
    i = 0
    for data in df['评分']:
        if data >= 4:
            posfile.write(str(df['评论'][i]) + '\n')
        elif data <= 2:
            negfile.write(str(df['评论'][i]) + '\n')
        i = i + 1
    # 2.利用snownlp训练新的模型
    sentiment.train(negpath, pospath)
    # 3.保存好新训练的模型
    sentiment.save(sentimentpath)
    print('训练完毕！模型已替换！')


# 三、SnowNLP分类函数
def SnowNLPTest(testPath):
    fp = open(testPath, "r", encoding='utf-8')
    lines = fp.readlines()
    k = 0
    m = 0
    score = 0  # 分类评分结果
    wb = xlwt.Workbook()
    ws = wb.add_sheet('test_sheet')
    wline = 1
    ws.write(0, 0, '评分')
    ws.write(0, 1, '评论')
    # 逐行读入评论
    for line in lines:
        try:
            s = SnowNLP(line)
            # 每条评论情感
            if len(line) > 1:  # 规避空白行
                if s.sentiments <= 0.2:
                    score = 1
                    ws.write(wline, 0, score)
                    ws.write(wline, 1, line)
                elif 0.2 < s.sentiments <= 0.4:
                    score = 2
                    ws.write(wline, 0, score)
                    ws.write(wline, 1, line)
                elif 0.4 < s.sentiments <= 0.6:
                    score = 3
                    ws.write(wline, 0, score)
                    ws.write(wline, 1, line)
                elif 0.6 < s.sentiments <= 0.8:
                    score = 4
                    ws.write(wline, 0, score)
                    ws.write(wline, 1, line)
                elif 0.8 < s.sentiments <= 1.0:
                    score = 5
                    ws.write(wline, 0, score)
                    ws.write(wline, 1, line)
                k = k + score
                m = m + 1
                wline = wline + 1
        except:
            print("")
    wb.save('D:/Users/Musk18/Desktop/4.测试集分类结果/测试结果.xls')
    if k / m <= 2.0:
        print('该部电影的总体情感分为:', round(k / m, 3), '观众的总体情感为:负面')
    elif 2.0 < k / m <= 4.0:
        print('该部电影的总体情感分为:', round(k / m, 3), '观众的总体情感为:中性')
    elif k / m >= 4.0:
        print('该部电影的总体情感分为:', round(k / m, 3), '观众的总体情感为:正面')
    print('分类结果已经保存在：', 'D:/Users/Musk18/Desktop/4.测试集分类结果/测试结果.xls')


if __name__ == '__main__':
    #     # 0.爬取数据
    #     SpiderPath = "D:/Users/Musk18/Desktop/1.爬取数据/"  # 爬取数据保存文件夹
    #     DOUBANPACHONG(26416155, SpiderPath)
    # 1.用训练集进行训练
    TrainPath = "D:/Users/Musk18/Desktop/2.训练集影评/"
    SnowNLP_TRAIN(TrainPath)
#     # 2.对测试集进行分类
#     testPath = r"D:/Users/Musk18/Desktop/1.爬取数据/纯影评.txt"
#     SnowNLPTest(testPath)