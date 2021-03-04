from wordcloud import WordCloud
import jieba
import jieba.analyse
import sys
import matplotlib.pyplot as plt

# 打开本体TXT文件
text = open('D:/Users/Musk18/Desktop/纯影评.txt',encoding='utf-8').read()

# 结巴分词 cut_all=True 设置为精准模式
wl_space_split = jieba.cut(text, cut_all=False)
# 设定allowPOS为‘a’（形容词），提取出情感词汇，进行词云输出
words = "  ".join(jieba.analyse.extract_tags(' '.join(wl_space_split), topK=200, withWeight=False, allowPOS=('a')))
words_list = words.split()
print(words_list)

# 去停用词,输出结果为outstr
stopwords = [line.strip() for line in open('D:/users/musk18/desktop/中文停用词表.txt',encoding='UTF-8').readlines()]
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
plt.savefig('D:/users/musk18/desktop/ciyun.png',dpi= 600, bbox_inches='tight',quality= 95)
plt.show()