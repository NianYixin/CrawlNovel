# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 16:19:18 2017

@author: Administrator
"""
import time
import downloader
import scraper
import dblink


def set_booklist_url(chanId=-1, page=1):
    '''
    main:generate the url of booklist page
    interpretation of param in URL:
    {
        size:Number of words, sign:does the book Already signed, tag:tag, 
        chanId:classification, subCateId:secondary classification, 
        orderId: update: page:page number, month:show book of Last three months 
        style:the style of UI. Tab or list?, 
        action:the state of book, vip:is vip?
    }
    '''
    
    url = (r"http://a.qidian.com/?size=-1&sign=2&tag=-1"
           r"&chanId={}&subCateId=-1&orderId=11&update=-1&page={}"
           r"&month=-1&style=2&action=-1&vip=-1".format(chanId,page))
    return url
    
def set_catalog_url(tokenId="", bookId=1):
    '''
    main:generate the url of [mvc get action] 
        to downlod the json data contain catalog infomation
    param in url:token and bookId
    '''

    url = (r"http://book.qidian.com/ajax/book/category"
           r"?_csrfToken={}"
           r"&bookId={}".format(tokenId,bookId))
    return url
    
def set_text_url(chapter):
    '''
    main:generate the url of content of novel
    '''

    url = (r"http://read.qidian.com/chapter/{}".format(chapter))
    return url
    
def write_html(html):
    file_new = open(r"tempfile\new.html", 'w', encoding='utf-8')
    file_new.write(html)
    file_new.close()
    
    
class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """
    def __init__(self, delay):
        self.delay = delay
        
    def wait(self):
        time.sleep(self.delay)

    
if __name__ == '__main__':
    downclass = downloader.Downloader()
    dbclass = dblink.MongoLink()
    html = downclass.urllib_download(set_booklist_url())
    scraperclass = scraper.Scraper(html)
    booklist = scraperclass.analysis_bookinfo()
    for eachbook in booklist:
        cataloglist = downclass\
            .send_getrequest(set_catalog_url(bookId=eachbook['bookid']))
        chapterlist = scraperclass.analysis_catalog(cataloglist)
        for eachchapter in chapterlist:
            chaptertext = downclass\
                .webkit_download(set_text_url(eachchapter))
            chaptertext = scraperclass.analysis_text(chaptertext)
            eachbook['text'] = chaptertext
            dbclass.save_to_db(eachbook)
            break
        break
    dbclass.read_by_line('index',1,1)
        
        
    
