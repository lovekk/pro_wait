from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.db.models import Count, F

from .models import Culture, CultureComment
from user.models import User

# 校园文化
def culture_content(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')
        skip = int(request.GET.get('skip'))
        end_skip = skip + 20  # 分页

        if school_id:
            # 浏览 +1
            look_this = Culture.objects.get(school=school_id)
            view_num = look_this.view_num + 1
            Culture.objects.filter(school=school_id).update(view_num=view_num)

            # 防止写入多个校园文化 选取最新的一个
            culture = Culture.objects.filter(school=school_id).values().order_by('-id')[0:1]
            # 学校id 用户id  ---->  用户昵称，用户头像, 评论id，评论内容
            culture_title = look_this.title
            comment = CultureComment.objects.filter(culture__title=culture_title,is_show=0).values(
                'content',
                'create_date',
                u_id=F('commentator__id'),
                u_nick=F('commentator__nick'),
                u_img=F('commentator__head_qn_url'),
            ).order_by('-id')[skip:end_skip]

            data = {}
            data['code'] = 200
            data['culture_data'] = list(culture)
            data['comment_data'] = list(comment)

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})
    else:
        return JsonResponse({'errmsg':'请求发生错误'})


# 添加评论
def add_comment(request):
    if request.method == 'POST':
        culture_id = request.POST.get('culture_id')
        comment = request.POST.get('comment')
        commentator_id = request.POST.get('commentator_id')

        user_in = User.objects.get(id=commentator_id)
        cul_in = Culture.objects.get(id=culture_id)
        CultureComment.objects.create(content=comment,culture=cul_in,commentator=user_in)

        # 评论 +1
        look_this = Culture.objects.get(id=culture_id)
        com_num = look_this.comment_num + 1
        Culture.objects.filter(id=culture_id).update(comment_num=com_num)

        return JsonResponse({'code':200})
    else:
        return JsonResponse({'errmsg':'提交评论失败'})



