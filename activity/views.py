from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.db.models import Count, F

from .models import Activity, ActivityComment
from user.models import User


#热门活动
def activity_list(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')
        skip = int(request.GET.get('skip'))
        if school_id:
            # 分页  10个一组
            end_skip = skip + 10
            activities = Activity.objects.filter(school=school_id, is_show=1).values(
                'id',
                'title',
                'small_img',
                'introduction',
                'publish_date',
                'host_unit',
                join_nums=Count('activitycomment')
            ).order_by('-id')[skip:end_skip]

            data = {}
            data['code']=200
            data['activity_data'] = list(activities)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})
    else:
        return JsonResponse({'errmsg':'请求发生错误'})


# 活动详情
def activity_detail(request):
    if request.method == 'GET':
        activity_id = request.GET.get('activity_id')
        skip = int(request.GET.get('skip'))
        end_skip = skip + 20  # 评论 分页
        if activity_id:

            # 浏览 +1
            look_this = Activity.objects.get(id=activity_id)
            view_num = look_this.view_num + 1
            Activity.objects.filter(id=activity_id).update(view_num=view_num)

            # 查询 详情和评论
            activity = Activity.objects.filter(id=activity_id).values()
            # 活动id 用户id  ---->  用户昵称，用户头像, 评论id，评论内容
            comment = ActivityComment.objects.filter(activity=activity_id).values(
                'commentator',
                'content',
                'comment_date',
                c_nick = F('commentator__nick'),
                c_head = F('commentator__head_image')
            ).order_by('-id')[skip:end_skip]

            data = {}
            data['code'] = 200
            data['activity_data'] = list(activity)
            data['comment_data'] = list(comment)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})
    else:
        return JsonResponse({'errmsg': '请求发生错误'})


# 添加评论
def add_comment(request):
    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        comment = request.POST.get('comment')
        commentator_id = request.POST.get('commentator_id')

        user_ins = User.objects.get(id=commentator_id)
        activity_ins = Activity.objects.get(id=activity_id)
        # culture_comment = CultureComment.objects.create(comment=comment,culture=cul_in,commentator=user_in)
        activity_comment = ActivityComment(content=comment)
        activity_comment.commentator = user_ins
        activity_comment.activity = activity_ins

        activity_comment.save()
        return JsonResponse({'code':200})
    else:
        return JsonResponse({'errmsg':'提交评论失败'})


