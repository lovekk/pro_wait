# -*- coding: utf-8 -*-
__author__ = 'super'
__date__ = '2018/12/20 21:46'

from lxml import etree
import requests
import urllib
from django.views.generic import View
from django.http import JsonResponse
from user.models import Cj,User,School

from base64 import b64encode

# 科文学院
# def set_session():
#     session = requests.session()
#     return session

session = requests.session()

# def getVIEWSTATE():
log_url = "http://202.195.67.232/jwgl/Login.aspx"
response = session.get(log_url)
# # 使用xpath获取__VIEWSTATE
selector = etree.HTML(response.content)
VIEWSTATE = selector.xpath('//*[@id="Form1"]/input/@value')[0]
VIEWSTATEGENERATOR = selector.xpath('//*[@id="Form1"]/input/@value')[1]
VENTVALIDATION = selector.xpath('//*[@id="Form1"]/input/@value')[2]

# 获取验证码并下载到本地
def getcode():
    img_url = "http://202.195.67.232/jwgl/other/CheckCode.aspx?datetime=az"
    imgresponse = session.get(img_url, stream=True)
    # print (session.cookies)
    image = imgresponse.content
    # 回去当前路径
    code = b64encode(image)
    return code

 # 定义登录的方法
def login(account,password,code):
    log_url = "http://202.195.67.232/jwgl/Login.aspx"
    data = {
        "__VIEWSTATE": VIEWSTATE,
        "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
        "__EVENTVALIDATION":VENTVALIDATION,
        "Account": account,
        "PWD": password,
        "CheckCode": code,
        "cmdok": ""
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    # 登陆教务系统
    response = session.post(log_url, data=data, headers=headers)
    # 获取学生姓名
    html = response.content.decode("gb2312")
    etree_html = etree.HTML(html)
    sname = etree_html.xpath("//table[@id='mainTbl']/tr[1]//span/text()")
    sname = " ".join(sname)
    return sname

#获取成绩
def getCj(user_id,school_id):
    cj_url = "http://202.195.67.232/jwgl/JWXS/cjcx/jwxs_cjcx_like.aspx"
    headers ={
        "Referer":"http://202.195.67.232/jwgl/JWXS/Default.aspx",
        "User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3)",
     }
    response = session.get(cj_url,headers=headers)
    html = response.content.decode("gb2312")
    etree_html = etree.HTML(html)
    trs = etree_html.xpath("//table[@id='cjxx']//tr[position()>1]")

    for tr in trs:
        td = tr.xpath("./td/text()")
        # 避免重复保存
        if Cj.objects.filter(daima=td[2],user=user_id).exists():
            print('数据已经存在，不能重复保存')
        else:
            u_ins=User.objects.get(id=user_id)
            school = School.objects.get(id=school_id)
            Cj.objects.create(daima=td[2], name=td[3], number=td[4], xueqi=td[1], is_pass=td[0], xuefen=td[5],leibie=td[8],user=u_ins,school=school)



