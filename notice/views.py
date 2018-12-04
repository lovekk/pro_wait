from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Notice

# 将公告信息传给前端

def notice_list(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')
        notice = Notice.objects.filter(school=school_id).values('id','title','publish_date')
        data = {}
        data['code'] = 200
        data['notice_data'] = list(notice)
        return JsonResponse(data)
    else:
        return JsonResponse({'errmsg':'请求发生错误'})

def notice_detail(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')
        notice_id = request.GET.get('notice_id')
        notice = Notice.objects.filter(school=school_id,id=notice_id).values()
        data = {}
        data['code'] = 200
        data['notice_data'] = list(notice)
        return JsonResponse(data)
    else:
        return JsonResponse({'errmsg': '请求发生错误'})


