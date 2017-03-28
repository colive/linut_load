#!/usr/bin/python
import urllib2
import urllib

def postHttp(dev='cpu',name='2',inner_ip=1):
    url='http://127.0.0.1:5000/load_feedback'
    user_agent="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36"
    headers={'User_Agent':user_agent,'Referer':'http://www.qiushibaike.com/hot/page/1'}
    postdata=dict(dev='cpu',name='2',inner_ip=1)
    print postdata
    dd=urllib.urlencode(postdata)
    request = urllib2.Request(url,urllib.urlencode({'dev':'cpu'}))
    response=urllib2.urlopen(request)
    print response.read()
postHttp()
