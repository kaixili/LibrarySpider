#!/usr/bin/env python
# coding=utf-8

import urllib.request
import urllib.parse
import re

def fetch(url):
    data = urllib.request.urlopen(url).read()
    data = data.decode('utf-8')  #请求网页信息并转码为utf-8
    
    info = []
                     #正则有一点长 以<span class="briefcitDetail">分界提取'书名''作者''出版信息''介绍'
    info = re.compile(\
        r'<span class="briefcitTitle">\n<a href=.*?">(.*?) / (.*?)</a>\n</span>\n<br />\n<span class="briefcitDetail">\n(.*?)\n<br />\n<span class="briefcitDetail">\n(.*?)<br />\n<br />\n<span class="briefcitDetail">\n(.*?)<br />'\
            ,re.DOTALL).findall(data)
    
    if info == []:         #搜索结果太详细就直接跳至详细页,提取信息方法改变
        info_not_red = re.sub('<font color="RED">', '', data)
        info_not_red = re.sub('</font>', '', info_not_red)      #去掉高亮代码
        info_not_red = re.sub('</strong>', '', info_not_red)
        info_not_red = re.sub('<strong>', '', info_not_red)
        
        info_t = info_p = info_n = []
        info_t = re.compile(\
            r'<tr><!-- next row for fieldtag=t -->\n.*?\n<td class="bibInfoData">\n(.*?) / (.*?)</td></tr>',re.DOTALL).findall(info_not_red)
        info_p = re.compile(\
            r'<tr><!-- next row for fieldtag=p -->\n.*?\n<td class="bibInfoData">\n(.*?)</td></tr>',re.DOTALL).findall(info_not_red)
        info_n = re.compile(\
            r'提要附注</td>\n<td class="bibInfoData">\n(.*?)</td></tr>',re.DOTALL).findall(info_not_red)
        
        info = info_t + info_p + info_n
        if info == []:print('无搜索结果,请改变关键词') #详细结果还没有结果,就没有结果
            
    return (info)


def nextpage(url0):
    data0 = urllib.request.urlopen(url0).read()
    data0 = data0.decode('utf-8')
    if re.search('后一页',data0):
        url_nextpage = re.compile(\
            r'<a href="(.*?)">后一页</a>',re.DOTALL).findall(data0)
        page = 'http://ftp.lib.hust.edu.cn/' + url_nextpage[0]
        select = input('存在下一页,按y\Y继续 \n 按其他键结束-->')
        if select == 'y' or select == 'Y':
             result(url)
        nextpage(url0)
    else:
        print('最后一页输出完毕\n')
        

def result(url):
    list = fetch(url) 
    lenth = len(list)
    for i in range(0, lenth):
        print(list[i])
    


###函数开始 输入后转码 进入第一页提取信息
if __name__ == '__main__':
    keyword = input("请输入关键词-->")
    keyword_quote = urllib.parse.quote(keyword)
    target = "http://ftp.lib.hust.edu.cn/search*chx/X?SEARCH="
    tail = "&SORT=D&image.x=0&image.y=0"

    url = target + keyword_quote + tail
    
    result(url)
    
    nextpage(url)

