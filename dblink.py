# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 21:05:21 2017

@author: Administrator
"""
import pymongo


class MongoLink(object):
    def __init__(self):
        self.client = pymongo.MongoClient('127.0.0.1', 27017)
        self.db=self.client.qidian_download
        #the index of books, use this collection to find out books in db
        self.index_table = self.db['index']
        
    def _save_to_index(self, dic):
        '''
        main:use method "save" to save infomation to qidian_download.index
        '''
        #print('save to index',type(dic),dic)
        self.index_table.save(dic)
        
    def save_to_db(self, dic):
        '''
        main:use method "save" to save text to collection named by bookid
        '''
        self.db[dic['bookid']].save(dic)
        dic.pop('text')
        self._save_to_index(dic)
    
    def read_by_line(self, table, skipline, limitline):
        '''
        main:return infomation by lsit order from qidian_download.index
        '''
        print(self.index_table.find_one())
        results = []
        for document in self.db[table].find(skip = skipline, limit = limitline):
            print('document:',document)
            results.append(document)
        return results

        
if __name__ == '__main__':
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db=client.qidian_download
    index = db['index']
    print(index.find_one())
    
    mg = MongoLink()
    #print(mg.read_by_line('index',1,10))
    if(False):
        aa=mg.db.get_collection('3676417')
        aa.find_one()
    print(mg.read_by_line('3676417',1,10))