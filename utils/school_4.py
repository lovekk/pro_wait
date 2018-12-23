# -*- coding: utf-8 -*-
__author__ = 'super'
__date__ = '2018/12/20 21:46'

import os
import re
from lxml import etree
import requests
import urllib
from django.views.generic import View
from django.http import JsonResponse

from base64 import b64encode

# 科文学院
def set_session(self):
    session = requests.session()
    return session

def getVIEWSTATE(self):
    log_url = "http://202.195.67.232/jwgl/Login.aspx"
    response = set_session().get(log_url)
    # # 使用xpath获取__VIEWSTATE
    selector = etree.HTML(response.content)
    __VIEWSTATE = selector.xpath('//*[@id="Form1"]/input/@value')[0]
    __VIEWSTATEGENERATOR = selector.xpath('//*[@id="Form1"]/input/@value')[1]
    __EVENTVALIDATION = selector.xpath('//*[@id="Form1"]/input/@value')[2]

# 获取验证码并下载到本地
def getcode():
    img_url = "http://202.195.67.232/jwgl/other/CheckCode.aspx?datetime=az"
    imgresponse = set_session().get(img_url, stream=True)
    # print (session.cookies)
    image = imgresponse.content
    # 回去当前路径
    code = b64encode(image)
    return JsonResponse({'code':code})

 # 定义登录的方法
def login(account,password,code):
    log_url = "http://202.195.67.232/jwgl/Login.aspx"
    data = {
        "__VIEWSTATE": getVIEWSTATE().__VIEWSTATE,
        "__VIEWSTATEGENERATOR": getVIEWSTATE().__VIEWSTATEGENERATOR,
        "__EVENTVALIDATION":getVIEWSTATE().__EVENTVALIDATION,
        "Account": account,
        "PWD": password,
        "CheckCode": code,
        "cmdok": ""
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    # 登陆教务系统
    response = set_session().post(log_url, data=data, headers=headers)
    # 获取学生姓名
    html = response.content.decode("gb2312")
    etree_html = etree.HTML(html)
    sname = etree_html.xpath("//table[@id='mainTbl']/tr[1]//span/text()")
    return sname
