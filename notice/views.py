from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Notice

# 将公告信息传给前端
# 公告列表
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


# 公告详情
def notice_detail(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')
        notice_id = request.GET.get('notice_id')
        if school_id and notice_id:

            # 浏览 +1
            look_this = Notice.objects.get(id=notice_id)
            view_num = look_this.view_num + 1
            Notice.objects.filter(id=notice_id).update(view_num=view_num)

            # 查询
            notice = Notice.objects.filter(school=school_id,id=notice_id).values()
            print(notice)
            data = {}
            data['code'] = 200
            data['notice_data'] = list(notice)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})
    else:
        return JsonResponse({'errmsg': '请求发生错误'})


