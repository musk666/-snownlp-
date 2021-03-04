import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba
import jieba.analyse
import sys
from pylab import *
from wordcloud import WordCloud
from sklearn.metrics import accuracy_score
#0.将评分为1,2的分为一类，3分为一类，4,5分为一类，共三类，再进行准确率计算
def secsort(L):
    y=[]
    for t in L:
        if t in [1,2]:
            y.append(1)
        elif t == 3:
            y.append(t)
        elif t in [4,5]:
            y.append(5)
    return y
# 1.柱状图输出
def plotout(readPath,savePath):
    # 解决patplotlib.pyplot图标中显示中文
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    train = pd.read_excel(readPath)
    y_pred = list(train['评分'])
    postive = 0
    general = 0
    negtive = 0
    for score in y_pred:
        if score <= 2 :
            negtive = negtive + 1
        elif score == 3 :
            general = general + 1
        elif 4 <= score <= 5:
            postive = postive + 1
    plt.figure(figsize=(10, 5))  # 设置画布的尺寸
    plt.title('电影评价情感分布图', fontsize=20)  # 标题，并设定字号大小
    plt.xlabel(u'情感', fontsize=14)  # 设置x轴，并设定字号大小
    plt.ylabel(u'数量', fontsize=14)  # 设置y轴，并设定字号大小
    # alpha：透明度；width：柱子的宽度；facecolor：柱子填充色；edgecolor：柱子轮廓色；lw：柱子轮廓的宽度；
    for a, b in zip(['负面', '中性', '正面'], [negtive,general,postive]):
        plt.text(a, b, b, ha='center', va='bottom')
    plt.bar(['负面', '中性', '正面'], [negtive,general,postive], alpha=0.6, width=0.8, facecolor='deeppink', edgecolor='darkblue', lw=1)
    plt.savefig(savePath,dpi= 600, bbox_inches='tight',quality= 95)
    plt.show()  # 显示图像
# 2.词云图输出
def ciyunout(readPath,savePath):
    # 打开本体TXT文件
#         train = pd.read_excel('D:/Users/Musk18/Desktop/4.测试集分类结果/测试结果.xls')
#         fn = open( 'D:/Users/Musk18/Desktop/4.测试集分类结果/neg.txt', "w", encoding='utf-8')
#         fg = open( 'D:/Users/Musk18/Desktop/4.测试集分类结果/gen.txt', "w", encoding='utf-8')
#         fp = open( 'D:/Users/Musk18/Desktop/4.测试集分类结果/pos.txt', "w", encoding='utf-8')
#         i = 0
#         for score in train['评分']:
#             if score <= 2 :
#                 fn.write(train['评论'][i]+ '\n')
#             elif score == 3 :
#                 fg.write(train['评论'][i]+ '\n')
#             elif 4 <= score <= 5:
#                 fp.write(train['评论'][i]+ '\n')
#             i = i + 1
        text = open('D:/Users/Musk18/Desktop/4.测试集分类结果/neg.txt',encoding='utf-8').read()
        # 结巴分词 cut_all=True 设置为精准模式
        wl_space_split = jieba.cut(text, cut_all=False)
        # 设定allowPOS为‘a’（形容词），提取出情感词汇，进行词云输出
        words = "  ".join(jieba.analyse.extract_tags(' '.join(wl_space_split), topK=200, withWeight=False, allowPOS=('a')))
        words_list = words.split()
        # 去停用词,输出结果为outstr
        stopwords = [line.strip() for line in open('D:/users/musk18/desktop/数据挖掘课设/中文停用词表.txt',encoding='UTF-8').readlines()]
        outstr = ''
        for word in words_list:
            if word not in stopwords:
                    if word != '\t':
                        outstr += word
                        outstr += " "
        # 对分词后的文本生成词云
        my_wordcloud = WordCloud(font_path='C:\windows\fonts\simhei.ttf',background_color= 'white', # 背景色为白色
        height= 400, # 高度设置为400
        width= 800, # 宽度设置为800
        scale= 20, # 长宽拉伸程度设置为20
        prefer_horizontal= 0.9999).generate(outstr)
        # 显示词云图
        plt.imshow(my_wordcloud)
        # 是否显示x轴、y轴下标
        plt.axis("off")
        plt.savefig(savePath,dpi= 600, bbox_inches='tight',quality= 95)
        plt.show()
if __name__ == '__main__':
    test = pd.read_excel('D:/Users/Musk18/Desktop/1.爬取数据/评分和影评.xls')
    train = pd.read_excel('D:/Users/Musk18/Desktop/4.测试集分类结果/测试结果.xls')
    true = list(test['评分'])
    pred = list(train['评分'])
    y_true = secsort(true)
    y_pred = secsort(pred)
    print("分类的准确率为：",round(accuracy_score(y_true,y_pred),2))
    readPath = 'D:/Users/Musk18/Desktop/4.测试集分类结果/测试结果.xls'
    savePath = 'D:/users/musk18/desktop/5.分类结果展示/电影评价情感分布图.png'
    plotout(readPath,savePath)
    readPath = 'D:/Users/Musk18/Desktop/1.爬取数据/纯影评.txt'
    savePath = 'D:/users/musk18/desktop/5.分类结果展示/词云图.png'
    ciyunout(readPath,savePath)
