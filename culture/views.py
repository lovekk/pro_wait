from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Culture

# 将校园文化传给前端
def culture_list(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')

        culture = Culture.objects.filter(school=school_id).values()
        data = {}
        data['code'] = 200
        data['article_data'] = list(culture)
        return JsonResponse(data)

    else:
        return JsonResponse({'errmsg':'请求发生错误'})

