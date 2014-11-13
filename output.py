#!/usr/bin/env python
# coding=utf-8
'''这是input函数的输入部分

   由input.py调用'''
import urllib.request
import re

def fetch(url):#抓取网页信息
    data = urllib.request.urlopen(url).read()
    data = data.decode('utf-8')  #请求网页信息并转码为utf-8
    
    global data_str
    data_str = str(data)  #使之变成str储存
    
    info = []
                     #正则有一点长 以<span class="briefcitDetail">分界提取'书名()''作者''出版信息''介绍'
    info = re.compile(\
        r'<span class="briefcitTitle">\n<a .*?">(.*?)</a>\n</span>\n<br />\n<span .*?>\n(.*?)\n<br />\n<span .*?>\n(.*?)<br />\n<br />\n<span.*?>\n(.*?)<br />'\
            ,re.DOTALL).findall(data)
    
    if info == []:                                       #搜索结果太详细就直接跳至详细页,提取信息方法改变
        info_not_red = re.sub('</*font.*?>', '', data_str)
        info_not_red = re.sub('</*strong>', '', info_not_red)#去掉高亮代码
        
        info_t = info_p = info_n = info_a = []
        info_t = re.compile(\
            r'题名</td>\n.*?\n(.*?)</td></tr>',re.DOTALL).findall(info_not_red)
        info_a = re.compile(\
            r'作者名</td>\n.*?\n<a.*?>(.*?)</a>',re.DOTALL).findall(info_not_red)
        info_p = re.compile(\
            r'出版发行</td>\n.*?\n(.*?)</td></tr>',re.DOTALL).findall(info_not_red)
        info_n = re.compile(\
            r'提要附注</td>\n.*?\n(.*?)</td></tr>',re.DOTALL).findall(info_not_red)
        info_n = [re.sub(r'&#34', ':', str(info_n))]      #发现引号问题 处理 最后以list输出
        
        if info_t: info = list(info_t[0]) + info_p + info_n
        if info == []:print('无搜索结果,请改变关键词')    #详细结果还没有结果,就没有结果
            
    return (info)


def nextpage(url):
    url_nextpage_tmp = re.compile(\
            r'结果页(.*?)">后一页</a>',re.DOTALL).findall(data_str)#如果存在返回2个相同的下一页网站
    
    if url_nextpage_tmp:
        url_nextpage = re.compile(\
            r'<a href="(.*?)$',re.DOTALL).findall(url_nextpage_tmp[1][-220:])
        page = 'http://ftp.lib.hust.edu.cn' + url_nextpage[0]    #下一页的页面提取
        select = input('存在下一页,按y\Y继续 \n 按其他键结束-->')
        if select == 'y' or select == 'Y':
            print('-------正在请求下一页内容-------------------')
            result_list(page)
            nextpage(page)
    else:
        print('======输出完毕=============\n')
        

def result_list(url):
    list = fetch(url) 
    lenth = len(list)
    for i in range(0, lenth):
        print(list[i])


