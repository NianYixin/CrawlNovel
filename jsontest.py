# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 23:28:40 2017

@author: Administrator
"""

class MyObj(object):

    def __init__(self,s):
        self.s = s

    def __repr__(self):

        return "<MyObj(%s)>" % self.s