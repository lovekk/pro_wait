from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Article

# 将文章显示到前端
def article_list(request):

    if request.method == 'GET':

        school_id = request.GET.get('school_id')

        articles = Article.objects.filter(school=school_id).values()
        data = {}
        data['code']=200
        data['article_data'] = list(articles)
        return JsonResponse(data)

    else:
        return JsonResponse({'errmsg':'请求发生错误'})


