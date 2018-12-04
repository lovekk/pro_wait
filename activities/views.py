from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Activites

#把热门活动相关信息传给前端
def activites_list(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')
        activites= Activites.objects.filter(school=school_id).values()
        data = {}
        data['code']=200
        data['article_data'] = list(activites)
        return JsonResponse(data)

    else:
        return JsonResponse({'errmsg':'请求发生错误'})


