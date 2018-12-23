# -*- coding: utf-8 -*-
__author__ = 'super'
__date__ = '2018/12/20 22:52'
import importlib

def getModule(school_id):
    school = 'school_' + school_id
    aa = importlib.import_module('utils.' + school)
    return aa
