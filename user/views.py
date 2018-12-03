from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import User,School


from django.db import connection

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

        obj = User.objects.filter(phone_num=phone_num).values('password')
        if (obj):
            for p in obj:
                pwd = p['password']
            if pwd == password:
                user_msg = User.objects.filter(phone_num=phone_num).values('id','nick','head_image')
                data = {}
                data['code'] = 200
                data['user_data'] = list(user_msg)
                return JsonResponse(data)
            else:
                return JsonResponse({'errmsg': '密码不正确'})
        else:
            return JsonResponse({'errmsg': '此手机号未注册'})
    else:
        return JsonResponse({'errmsg':'请求发生错误'})


# 注册
def register(request):
    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')

        user = User(phone_num=phone_num,password=password)
        user.save()
        user_id = User.objects.filter(phone_num=phone_num).values('id')
        data = {}
        data['list'] = list(user_id)
        return JsonResponse(data)
    else:
        return JsonResponse({'errmsg':'发生错误'})


# 注册 用户名 性别 学校 头像上传
def register_msg(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        nick = request.POST.get('nick')
        gender = request.POST.get('gender')
        school_id = 4
        school_name = '江苏师范大学'
        head_image = request.FILES.get('head_image')

        User.objects.filter(id=uid).update(
            nick=nick,
            gender=gender,
            school_id=school_id,
            school_name=school_name,
            head_image=head_image,
        )

        head_image = User.objects.filter(id=uid).values('head_image')
        for h in head_image:
            head = h
            print(head)

        head_image_url = 'http://192.168.0.106:8000/media/' + head['head_image']
        return JsonResponse({'head_image_url':head_image_url})
    else:
        return JsonResponse({'errmsg':'发生错误'})


# 学校列表
def school_list(request):
    if request.method == 'GET':
        school_list = School.objects.filter(is_show=True).values('id','name')
        data = {}
        data['code'] = 200
        data['list'] = list(school_list)
        return JsonResponse(data)
    else:
        return JsonResponse({'errmsg':'发生错误'})