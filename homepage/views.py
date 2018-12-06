
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from activity.models import Activity
from article.models import Article

# Create your views here.

# 首页准备数据
# 校园活动 轮播图3张 id big_img
# 文章推荐 最新的前5篇
def index_list(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')
        if school_id :
            # id倒序前3个 首页轮播图就3张
            activity= Activity.objects.filter(school=school_id,is_first=1).values('id','big_img').order_by('-id')[0:3]
            # id倒序前5个 显示5篇
            article = Article.objects.filter(school=school_id).values('id','title', 'list_img', 'author','publish_date').order_by('-id')[0:5]
            data = {}
            data['code'] = 200
            data['activity'] = list(activity)
            data['article'] = list(article)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})
    else:
        return JsonResponse({'errmsg':'请求发生错误'})


