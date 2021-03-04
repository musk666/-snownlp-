import requests
import time
import xlwt
import pandas as pd
from lxml import etree

from wordcloud import WordCloud
import jieba
import sys
import matplotlib.pyplot as plt

# 0.指定输出文本保存路径
path = "C:\\Users\\Musk18\\Desktop\\纯影评.txt"  #
wb = xlwt.Workbook()
ws = wb.add_sheet('test_sheet')
wline = 0
# 1.对电影评论及其评分进行爬取(200条)
for i in range(0,10):
    url = 'https://movie.douban.com/subject/30402296/comments?start={}&limit=20&sort=new_score&status=P'.format(i*20)
    headers = {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0)Gecko/20100101 Firefox/66.0"
          }
    session = requests.Session()
    response = session.get(url, headers=headers)
    page_code = response.text
    html = etree.HTML(page_code)
    # 1.1对评论进行提取并且保存在execl里，纯评论保存在txt里
    pinglun = html.xpath('//*[@id="comments"]/div/div[2]/p/span/text()')  # 筛选评论
    pingfen = html.xpath('.//*[@class="comment-info"]//span[2]/@title')  # 筛选评分
    pdict={'很差': '☆', '较差': '☆☆', '还行': '☆☆☆', '推荐': '☆☆☆☆', '力荐': '☆☆☆☆☆'}  # 建立字典来映射评价和星星数的关系
    for j, k in zip(pingfen, pinglun):
        with open(path, 'a', encoding='utf-8') as f:
            if j in pdict:  # 这一句话的目的是规避没有进行评分的评论，无评分评论应该被视作无效评论
                xingxing = pdict[j]
                f.write(k+'\n')
                ws.write(wline, 0, xingxing)
                ws.write(wline, 1, k)
                wline=wline+1
    wb.save('C:/Users/Musk18/Desktop/评分和影评.xls')  # 将爬取的数据保存到影评.xls
    time.sleep(3)  # 设置一个爬取延时，防止被检测爬虫
    print("下载第{}页数据完毕！\n".format(i + 1))


