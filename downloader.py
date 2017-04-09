# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 21:07:38 2017

@author: Administrator
"""
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebView
import sys
import urllib
import requests


class Downloader(object):
    '''
    main:The function of this class is to download web pages
    Provide ways: 
        {
            urllib_download:use urllib Vulnerable to the ajax 
            webkit_download:use WebKit of PyQt, cost long time 
        }
    '''
    def urllib_download(self, url, num_retries=2):
        try:
            headers = {'User-Agent':'Mozilla/5.0 \
                       (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) \
                       Gecko/20091201 Firefox/3.5.6'}
            req = urllib.request.Request(url,headers=headers) 
            response = urllib.request.urlopen(req)
            html = response.read()
            return html.decode('utf8')
        except :
            print("Unexpected error:", sys.exc_info()[0])
            if(num_retries>0):
                if(hasattr(sys.exc_info()[1],"code") and
                   500<=sys.exc_info()[1].code<600):
                    return self.urllib_download(url,num_retries-1)
        else:
            print("no expected")
        finally:
            print("executing finally clause")
            
    def webkit_download(self, url):
        app = QApplication([])
        webview = QWebView()
        webview.loadFinished.connect(app.quit)
        webview.load(QUrl(url))
        app.exec_() # delay here until download finished
        return webview.page().mainFrame().toHtml()
        
    def send_getrequest_2(self, url):
        headers = {'User-Agent':'Mozilla/5.0 \
                       (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) \
                       Gecko/20091201 Firefox/3.5.6'}
        req = urllib.request.Request(url,headers=headers) 
        response = urllib.request.urlopen(req)
        html = response.read()
        return html.decode()
            
    def send_getrequest(self, url):
        req = requests.get(url)  
        if req.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding
        encode_content = req.content.\
            decode(encoding, 'replace').encode('utf-8', 'replace')
        return encode_content.decode()



