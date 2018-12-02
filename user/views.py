from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import User,School


# 测试首页
def index(request):
    return HttpResponse('ok')


# 测试json
def test_json(request):
    return JsonResponse({'name':'zk', 'num':123456})


# 注册
def register(request):
    if request.method == 'POST':
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')

        user = User(phone_num=telephone,password=password)
        user.save()
        user_id = User.objects.filter(phone_num=telephone).values('id')
        data = {}
        data['list'] = list(user_id)
        return JsonResponse(data)
    else:
        return JsonResponse({'id':1})


# 注册 用户名 性别 学校
def register_mes(request):
    pass


# 注册 上传头像
def register_head(request):
    if request.method == 'POST':

        uid = request.POST.get('id')
        print(uid)
        headimage = request.FILES.get('headimage')

        User.objects.filter(id=uid).update(headimage=headimage)

        headimage_url = User.objects.filter(id=uid).values('headimage')
        for h in headimage_url:
            head = h

        image_url = 'http://192.168.0.109:8000/media/' + head['headimage']
        print(image_url)

        return JsonResponse({'image_url':image_url})
    else:
        return JsonResponse({'message':'fail'})





# 学校列表
def school_list(request):
    if request.method == 'GET':
        school_list = School.objects.filter(is_show=True).values('id','name')
        data = {}
        data['code'] = 200
        data['list'] = list(school_list)
        return JsonResponse(data)
    else:
        return JsonResponse({'code':404})