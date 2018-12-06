from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.db.models import F

from article.models import Article, ArticleComment
from user.models import User

# 文章列表
def article_list(request):

    if request.method == 'GET':
        school_id = request.GET.get('school_id')
        if school_id :
            articles = Article.objects.filter(school=school_id,is_show=1).values('id', 'title', 'author', 'publish_date', 'list_img')
            data = {}
            data['code']=200
            data['article_data'] = list(articles)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})
    else:
        return JsonResponse({'errmsg':'请求发生错误'})


# 文章详情 评论
def article_detail(request):
    if request.method == 'GET':
        article_id = request.GET.get('article_id')
        if article_id:
            # 浏览 +1
            look_this = Article.objects.get(id=article_id)
            view_num = look_this.view_num + 1
            Article.objects.filter(id=article_id).update(view_num=view_num)

            # 查询 详情
            article = Article.objects.filter(id=article_id).values()

            # 文章id 用户id  ---->  用户昵称，用户头像, 评论id，评论内容，评论时间
            # print(article_id)
            comment = ArticleComment.objects.filter(article=article_id).values(
                'commentator',
                'content',
                'create_date',
                c_nick=F('commentator__nick'),
                c_head=F('commentator__head_image')
            ).order_by('-id')
            # print(list(comment))
            data = {}
            data['code'] = 200
            data['article_data'] = list(article)
            data['comment_data'] = list(comment)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})
    else:
        return JsonResponse({'errmsg': '请求发生错误'})



# 添加评论
def add_comment(request):
    if request.method == 'POST':
        # 获取post数据
        article_id = request.POST.get('article_id')
        comment = request.POST.get('comment')
        commentator_id = request.POST.get('commentator_id')
        # 创建外键实例
        user_ins = User.objects.get(id=commentator_id)
        article_ins = Article.objects.get(id=article_id)
        # 保存数据
        article_comment = ArticleComment(content=comment)
        article_comment.commentator = user_ins
        article_comment.article = article_ins
        article_comment.save()
        return JsonResponse({'code':200})
    else:
        return JsonResponse({'errmsg':'提交评论失败'})


