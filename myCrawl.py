# -*- coding: utf-8 -*-
import urllib2
import sys
import urlparse
import re
import time
from bs4 import BeautifulSoup
sys_encoding = sys.getfilesystemencoding()


def download(url,user_agent = 'wswp',num_retries = 2): 
    #如果错误码5xx 需要重新下载
    print 'Downloading:',url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url,headers = headers)
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e,'code') and 500<=e.code<600:
                return download(url,num_retries-1)
    #print html
    return html
if __name__ == "__main__":

    reload(sys) 
    sys.setdefaultencoding('utf-8')
    name = raw_input('PLZ input username of CSDN:')
    html = download("https://blog.csdn.net/"+name)
    soup = BeautifulSoup(html,features="lxml")
    soup = soup.find(attrs={'class':'article-list'})
    
    links=set(re.compile('(data-articleid=")+(.*)',re.IGNORECASE).findall(str(soup)))
   
    for link in links:
        if re.compile('style="display: none;',re.IGNORECASE).findall(str(link)):#去掉隐藏的文章
            continue
        

        url='https://blog.csdn.net/Protocols7/article/details/'+str(link[1][0:8])
        html = download(url)
        soup = BeautifulSoup(html,features="lxml")
        title = soup.find(attrs={'class':'title-article'})
        text = soup.find(attrs = {'id':'content_views'})
        filename = title.text.encode('gb2312').replace('\\','&').replace('/','&')
        
       
        print ("Writing:"+filename+".md")
        f = open('src/'+filename+'.md','w')
        f.write("---\ntitle: " +title.text+ "\ndate: "+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"\ntags: None\n---\n")
        f.write(str(text))
        f.close()
    print("Done!")





    

