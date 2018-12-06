from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Culture, CultureComment
from user.models import User

# 校园文化
def culture_content(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')

        if school_id:
            # 浏览 +1
            look_this = Culture.objects.get(school=school_id)
            view_num = look_this.view_num + 1
            Culture.objects.filter(school=school_id).update(view_num=view_num)

            # 防止写入多个校园文化 选取最新的一个
            culture = Culture.objects.filter(school=school_id).values().order_by('-id')[0:1]
            # 学校id 用户id  ---->  用户昵称，用户头像, 评论id，评论内容
            culture_title = look_this.title
            comment = CultureComment.objects.filter(culture__title=culture_title).values(
                'commentator',
                'content',
                'create_date',
                'commentator__nick',
                 'commentator__head_image'
            ).order_by('-id')

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
        print(culture_id)
        print(comment)
        print(commentator_id)

        user_in = User.objects.get(id=commentator_id)
        cul_in = Culture.objects.get(id=culture_id)
        # culture_comment = CultureComment.objects.create(comment=comment,culture=cul_in,commentator=user_in)
        culture_comment = CultureComment(content=comment)
        culture_comment.commentator = user_in
        culture_comment.culture = cul_in

        culture_comment.save()
        return JsonResponse({'code':200})
    else:
        return JsonResponse({'errmsg':'提交评论失败'})



