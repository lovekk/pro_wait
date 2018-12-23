from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import connection
from django.views.generic import View

from .models import User, School

import importlib
from utils.getModule import getModule
from utils.qiniu_upload import qi_local_upload, qi_upload

from pro_wait.settings import MEDIA_ROOT

import hashlib


# 测试首页
def index(request):
    return HttpResponse('ok')


# 测试json
def test_json(request):
    return JsonResponse({'name':'zk', 'num':123456})


# 用户登录
def login(request):

    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')

        password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        obj = list(User.objects.filter(phone_num=phone_num).values('password'))
        if (obj):
            pwd = obj[0].get('password')
            print(pwd)
            print(password_md5)
            if str(pwd) == str(password_md5):
                user_msg = User.objects.filter(phone_num=phone_num).values('id','nick','head_image','head_qn_url','school','token')
                data = {}
                data['code'] = 200
                data['user_data'] = list(user_msg)
                print(data)
                return JsonResponse(data)
            else:
                return JsonResponse({'errmsg': '密码不正确'})
        else:
            return JsonResponse({'errmsg': '此手机号未注册'})
    else:
        return JsonResponse({'errmsg':'请求发生错误'})


# 注册手机号是否已经使用
def register(request):
    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        is_have = User.objects.filter(phone_num=phone_num).exists()
        if is_have:
            return JsonResponse({'errmsg': '此手机号已经注册，可以直接登录'})
        else:
            return JsonResponse({'code': 200})
    else:
        return JsonResponse({'errmsg':'发生错误'})


# 注册 用户名 性别 学校 头像上传
def register_msg(request):
    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')
        password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()

        nick = request.POST.get('nick')
        gender = request.POST.get('gender')
        school_id = request.POST.get('school_id')
        school_name = request.POST.get('school_name')

        device_num = request.POST.get('device_num')
        device_model = request.POST.get('device_model')
        device_name = request.POST.get('device_name')
        operator = request.POST.get('operator')

        head_image = request.FILES.get('head_image')
        print(head_image)

        # 等号+1
        ac_num = list(User.objects.values('account_num').order_by('-id')[0:1])
        account_num = int(ac_num[0].get('account_num')) + 1
        print(account_num)

        # 先更新用户信息
        if phone_num and password and nick and head_image and school_id:
            user_create = User.objects.create(
                phone_num=phone_num,
                password=password_md5,
                nick=nick,
                gender=gender,
                school_id=school_id,
                account_num=account_num,
                school_name=school_name,
                device_num=device_num,
                device_model=device_model,
                device_name=device_name,
                operator=operator,
                head_image=head_image
            )
            data = {}
            if user_create:
                # 先保存到本地 不保存七牛 因为直接用七牛的put_data提示报错 期望不是InMemoryUploadedFile类型
                # 下面做七牛保存
                user_local_img = str(MEDIA_ROOT) + '/' + str(user_create.head_image)  # 拼接本地绝对路径
                qi_local_img = qi_local_upload(user_local_img)  # 七牛上传
                User.objects.filter(id=user_create.id).update(head_qn_url=qi_local_img)  # 更新七牛数据
                # 查询用户信息返回
                user_msg = User.objects.filter(id=user_create.id).values('id','nick','head_image','head_qn_url','school__id','school__name')

                # 返回用户信息
                data['code'] = 200
                data['user_msg'] = list(user_msg)

                print(data)
                return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '注册信息不全！'})
    else:
        return JsonResponse({'errmsg':'发生未知错误！'})
# 测试为什么update不行 不能更新图片
# def register_msg(request):
#     if request.method == 'POST':
#
#         head_image = request.FILES.get('head_image')
#         print(head_image)
#
#         pic = User.objects.get(id=13)
#         pic.head_image = head_image
#         pic.save()
#
#         return JsonResponse({'code':200})
#
#     else:
#         return JsonResponse({'errmsg':'发生错误'})


# 我的页面 个人信息


# 学校列表
def school_list(request):
    if request.method == 'GET':
        school_list = School.objects.filter(is_show=True).values('id','name','province','city')
        data = {}
        data['code'] = 200
        data['list'] = list(school_list)
        return JsonResponse(data)
    else:
        return JsonResponse({'errmsg':'发生错误'})
    
    
# 学生认证
class SchoolAuth(View):
    def post(self, request):
        school_id = request.POST.get('school_id')
        user_id = request.POST.get('user_id')
        account = request.POST.get('account')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if account and password and code:
            module = getModule(school_id)
            u_name = module.login(account,password,code)
            print(u_name)
            if u_name:
                User.objects.filter(id=user_id).update(real_name=u_name,stu_num=account,stu_password=password,is_school_auth=1)
            else:
                return JsonResponse({"errmsg":"信息输入错误"})
        else:
            return JsonResponse({"errmsg":"没接收到学号或者密码"})


# # 返回验证码图片
# # def getCodeImage(request):
# #     if request.method == 'POST':
# #         school_id = request.POST.get('school_id')
# #         module = getModule(school_id)
# #         module.getcode()


# 更新token
class UserToken(View):
    def post(self, request):
        user_id = request.POST.get('user_id')
        user_token = request.POST.get('user_token')
        if user_id and user_token:
            User.objects.filter(id=user_id).update(token=user_token)
            return JsonResponse({"code": 200})
        else:
            return JsonResponse({"errmsg":"没接收到"})