from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_POST,require_GET
from django.db.models import Count, F
from django.views.generic import View

from utils.qiniu_upload import qi_upload, qi_local_upload

from lose.models import Lose, LoseImg, LoseComment, LoseReplyComment
from user.models import User, School

import time, os, copy
from pro_wait.settings import MEDIA_ROOT

# Create your views here.


# 失物招领 列表  现在使用的是这种写法
@require_GET
def lose_list(request):
    school_id = request.GET.get('school_id')
    skip = int(request.GET.get('skip'))
    if school_id:
        # 一对多 反查外键
        # 先查询 所有id
        end_skip = skip + 10
        loses_first = Lose.objects.filter(school=school_id,is_show=0).values('id').order_by('-id')[skip:end_skip]

        data = {}
        for_all = {}   # 单次数据
        all_list = []   # 总数据

        # 遍历id
        for item in list(loses_first):
            # print(item.get('id'))  # {'id': 43}
            item_id=item.get('id')
            # 查发布内容
            for_t = Lose.objects.filter(id=item_id).values('id', 'content', 'good_num', 'create_date', 'create_time',
                'is_type', 'view_num', u_nick = F('creator__nick'), u_img = F('creator__head_qn_url'),
                u_id = F('creator__id'), u_token = F('creator__token'))

            for_text = list(for_t)
            # 查发布图片
            for_img = list(LoseImg.objects.filter(lose=item_id).values('id', 'qiniu_img','lose'))

            for_all['id'] = item_id
            for_all['for_text'] = for_text
            for_all['for_img'] = for_img

            all_list.append(copy.deepcopy(for_all))
            # print(for_all)

        data['code'] = 200
        data['show_list'] = all_list

        return JsonResponse(data)
    else:
        return JsonResponse({'errmsg': '尚未选择学校'})


# 失物招领 列表 这种写法不如上面的好些,使用的上面的写法
class IndexView(View):
    def get(self, request):
        school_id = request.GET.get('school_id')
        if school_id:
            # 一对多 反查外键
            # 先查询 所有id
            loses_first = Lose.objects.filter(school=school_id, is_show=0).values('id', 'content','view_num',
                'good_num', 'create_date', 'create_time', 'is_type', u_nick=F('creator__nick'),
                u_img=F('creator__head_qn_url'), u_id=F('creator__id')).order_by('-id')

            data = {}
            for_all = {}  # 单次数据
            all_list = []  # 总数据

            # 遍历id
            for item in list(loses_first):
                # print(item.get('id'))  # {'id': 43}
                item_id = item.get('id')
                # 查发布图片
                for_all['for_img'] = list(LoseImg.objects.filter(lose=item_id).values('id', 'qiniu_img', 'lose'))
                all_list.append(copy.deepcopy(for_all))
                # print(for_all)

            data['code'] = 200
            data['text_list'] = list(loses_first)
            data['img_list'] = all_list

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 添加 发布 失物招领
@require_POST
def lose_add(request):
    # 获取ajax数据
    school_id = request.POST.get('school_id')
    content = request.POST.get('content')
    creator_id = request.POST.get('creator_id')
    is_type = request.POST.get('is_type')

    # 获取ajax图片
    img_list = request.FILES.getlist('img_list')

    time_stamp = time.time()  # 多余了  本来是想用时间戳作为 唯一标识的

    if school_id and creator_id:
        # 保存文本数据
        user_ins = User.objects.get(id=creator_id)
        school_ins = School.objects.get(id=school_id)
        lose_create = Lose.objects.create(content=content, is_type=is_type, school=school_ins, creator=user_ins)

        # 保存 外键的 图片数据
        # 这一块 写的 绝望
        if img_list:
            for img in img_list:
                # 先保存到本地 不保存七牛 因为直接用七牛的put_data提示报错 期望不是InMemoryUploadedFile类型
                # 不怕图片名称重复 django处理了
                save_img = LoseImg.objects.create(local_img=img, lose=lose_create)

                # 下面做七牛保存
                lose_local_img = str(MEDIA_ROOT) + '/' + str(save_img.local_img)   # 拼接本地绝对路径
                lose_img_id = save_img.id   # 获取当前本地图片的id
                qi_local_img = qi_local_upload(lose_local_img)  # 七牛上传
                LoseImg.objects.filter(id=lose_img_id).update(qiniu_img=qi_local_img)   # 更新七牛数据

        return JsonResponse({'code':200})
    else:
        return JsonResponse({'errmsg': '上传保存失败'})


#  失物招领 详情
class LoseDetailView(View):
    def get(self, request):
        lose_id = request.GET.get('lose_id')

        if lose_id:
            # 浏览 +1
            look_this = Lose.objects.get(id=lose_id)
            view_num = look_this.view_num + 1
            Lose.objects.filter(id=lose_id).update(view_num=view_num)

            # ======================================失物招领详情================================
            # 查询 详情和评论
            lose = Lose.objects.filter(id=lose_id,is_show=0).values(
                'id',
                'content',
                'view_num',
                'create_date',
                'create_time',
                'is_type',
                c_id=F('creator__id'),
                c_nick=F('creator__nick'),
                c_head=F('creator__head_qn_url')
            )

            # 查发布图片
            img = list(LoseImg.objects.filter(lose=lose_id).values('id', 'qiniu_img', 'lose'))

            # ======================================失物招领· 留言================================
            # 失物招领id 用户id  ---->  用户昵称，用户头像, 评论id，评论内容,排序
            comment = LoseComment.objects.filter(lose=lose_id,is_show=0).values(
                'id',
                'user',
                'content',
                'comment_time',
                'comment_date',
                c_id=F('user__id'),
                c_nick=F('user__nick'),
                c_head=F('user__head_qn_url')
            ).order_by('-id')

            data = {}
            # 将每个二级评论添加到对应的一级评论上
            for item in list(comment):
                # 获取一级评论id
                comment_id = item.get('id')
                one_replay = LoseReplyComment.objects.filter(comment=comment_id).values(
                    'id', 'content', p_nick=F('parent__user__nick'), c_nick=F('user__nick'), c_id=F('user__id')
                ).order_by('id')
                # 字典
                item['replycomment'] = list(one_replay)

            data['code'] = 200
            data['lose_data'] = list(lose)
            data['img'] = list(img)
            data['comment_data'] = list(comment)

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '请求发生错误'})


# 添加 一级评论
class AddCommentView(View):
    def post(self, request):
        lose_id = request.POST.get('lose_id')
        user_id = request.POST.get('user_id')
        content = request.POST.get('content')

        if lose_id and user_id:
            user_ins = User.objects.get(id=user_id)
            lose_ins = Lose.objects.get(id=lose_id)

            LoseComment.objects.create(content=content, user=user_ins, lose=lose_ins)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'msg': '数据未保存成功！'})


# 添加 二级评论
class ReplyCommentView(View):
    def post(self, request):
        comment_id = request.POST.get('comment_id')
        user_id = request.POST.get('user_id')
        lose_id = request.POST.get('lose_id')
        reply_id = request.POST.get('reply_id')

        reply_content = request.POST.get('reply_content')

        user_ins = User.objects.get(id=user_id)
        comment_ins = LoseComment.objects.get(id=comment_id)
        lose_ins = Lose.objects.get(id=lose_id)

        # 如果是 回复的回复
        if reply_id:
            comment_reply_ins = LoseReplyComment.objects.get(id=reply_id)
            reply_comment = LoseReplyComment.objects.create(content=reply_content, user=user_ins, lose=lose_ins,
                                                              comment=comment_ins, parent=comment_reply_ins)
        else:
            reply_comment = LoseReplyComment.objects.create(content=reply_content, user=user_ins, lose=lose_ins,
                                                              comment=comment_ins)

        if reply_comment:
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '数据没有保存成功！'})











