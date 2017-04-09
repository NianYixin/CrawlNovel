# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 21:06:36 2017

@author: Administrator
"""
import re
import json
import lxml.html
import lxml.etree


class Scraper(object):
    def __init__(self,html):
        self.tree = lxml.html.fromstring(html)
        
    def analysis_bookinfo(self):
        '''
        main: analysis the booklist and get a list of dictionary
        example: [{bookname:aaa,author:bbb,bookid:ccc},{...}]
        '''
        results = []
        selector_expression=(r"table > tbody > "
                             r"tr:nth-child({}) > "
                             r"td:nth-child({}) > a")
        
        def _len_of_booklist():
            '''get the length of the booklist'''
            tbody=self.tree.cssselect(r"table > tbody")[0]
            return len(tbody.findall('tr'))
        
        def _analysis_line(tr):
            book = self.tree.cssselect(selector_expression.format(tr, 2))[0]
            re_bookid = r"info/([0-9]+)"
            dic = {}
            dic['bookname'] = str(book.text_content())
            dic['bookid'] = re.findall(re_bookid, book.attrib['href'])[0]
            author = self.tree.cssselect(selector_expression.format(tr, 5))[0]
            dic['bookauthor'] = str(author.text_content())
            
            results.append(dic)
        
        for number in range(1,_len_of_booklist()+1):
            _analysis_line(number)
        
        return results
        
    def analysis_catalog(self, cataloglist):
        results = set()
        '''
        main:get the lsit of path about chapter from a Json data
        '''
        catalogjson=json.loads(cataloglist)
        #from all get path
        data=catalogjson['data']
        vs=data['vs']
        for each in vs:
            #free? when hS==True, I should pay for it 
            if(each['hS'] == True):
                continue
            for everyone in each['cs']:
                results.add(everyone['cU'])
        return results
        
    def analysis_text(self, text):
        text_tree = lxml.html.fromstring(text)
        results = text_tree\
            .cssselect('div.read-content.j_readContent > p')
        text = ''
        for each in results:
            text += str(each.text_content()) + '\n'
        return text
        
        
if __name__ == '__main__':
    f = open(r'tempfile\text.html','r',encoding='utf8')
    s = f.read()
    f.close()
    scr = Scraper(s)
    a = scr.analysis_text(s)

