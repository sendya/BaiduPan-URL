#-*- coding:utf-8 -*-

import web
import os
import urllib2
import re

web.config.debug = False

PAN_USER_AGENT = 'JUC(Linux;U;2.2;Zh_cn;HTC Desire;480*800;)UCWEB7.7.0.85/139/999'
PAN_REGEX = r'href=\"(http\:\/\/d\.pcs\.baidu\.com\S*)\"\sid='

#更新原文件
# + BaiduPan2 正则
urls = (
    r'/(\d+)v(\d+)\.\w+', 'BaiduPan',
	r'/(\w{6}).\w+', 'BaiduPan2',
    r'/(.*)', 'Index',
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class Index:        
    def GET(self, arg):
         web.seeother('/web/durl.html')

def BaiduPanRealUrl(shareid, uk):
    url = 'http://pan.baidu.com/share/link?shareid=' + shareid + '&uk=' + uk
    baidu_request = urllib2.Request(url)
    baidu_request.add_header('User-Agent', PAN_USER_AGENT)
    data = urllib2.urlopen(baidu_request).read()
    regex = re.compile(PAN_REGEX)
    match = re.search(regex, data)
    if match:
        new_url = match.group(1).replace('amp;', '')
        if new_url.startswith('http'):
            return new_url
    raise web.notfound()

def BaiduPanRealUrlB(shareid):
    url = 'http://pan.baidu.com/s/' + shareid
    baidu_request = urllib2.Request(url)
    baidu_request.add_header('User-Agent', PAN_USER_AGENT)
    data = urllib2.urlopen(baidu_request).read()
    regex = re.compile(PAN_REGEX)
    match = re.search(regex, data)
    if match:
        new_url = match.group(1).replace('amp;', '')
        if new_url.startswith('http'):
            return new_url
    raise web.notfound()
	
class BaiduPan:
    def GET(self, shareid, uk):
        if (shareid.isdigit() and uk.isdigit()):
            return web.redirect(BaiduPanRealUrl(shareid, uk))
        else:
            return web.notfound()
          
# 新版度盘分享链接转换代码 
class BaiduPan2:
    def GET(self, shareid):
      if(shareid.isalnum()):
            return web.redirect(BaiduPanRealUrlB(shareid))
      else:
            return web.notfound()
        
app = web.application(urls, globals()).wsgifunc()

from bae.core.wsgi import WSGIApplication 
application = WSGIApplication(app)
