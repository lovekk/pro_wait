from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_POST,require_GET
from django.db.models import Count, F

from utils.qiniu_upload import qi_upload, qi_local_upload

from lose.models import Lose, LoseImg
from user.models import User, School

import time, os, copy
from pro_wait.settings import MEDIA_ROOT
# Create your views here.


# 失物招领 列表
@require_GET
def lose_list(request):
    school_id = request.GET.get('school_id')
    if school_id:
        # 一对多 反查外键
        # 先查询 所有id
        loses_first = Lose.objects.filter(school=school_id, is_first=0).values('id').order_by('-id')

        data = {}
        for_all = {}   # 单次数据
        all_list = []   # 总数据

        # 遍历id
        for item in list(loses_first):
            # print(item.get('id'))  # {'id': 43}
            item_id=item.get('id')
            # 查发布内容
            for_t = Lose.objects.filter(id=item_id).values('id', 'content', 'good_num', 'create_date', 'create_time', 'is_type',
                u_nick = F('creator__nick'), u_img = F('creator__head_qn_url'), u_id = F('creator__id'), u_token = F('creator__token'))
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
        lose_create = Lose.objects.create(content=content, is_type=is_type, time_stamp=time_stamp, school=school_ins, creator=user_ins)

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





#热门活动
# def lose_list(request):
#     if request.method == 'GET':
#         school_id = request.GET.get('school_id')
#         if school_id:
#             # 一对多 反查外键
#             # 先查询 所有id
#             loses_first = Lose.objects.filter(school=school_id, is_first=0).values('id').order_by('-id')
#
#             data = {}
#             for_all = {}  # 单次数据
#             all_list = []  # 总数据
#
#             # 遍历id
#             for item in list(loses_first):
#                 # print(item.get('id'))  # {'id': 43}
#                 item_id = item.get('id')
#                 # 查发布内容
#                 for_t = Lose.objects.filter(id=item_id).values('id', 'content', 'good_num', 'create_date',
#                                                                'create_time', 'is_type',
#                                                                u_nick=F('creator__nick'),
#                                                                u_img=F('creator__head_image'), u_id=F('creator__id'),
#                                                                u_token=F('creator__token'))
#                 for_text = list(for_t)
#                 # 查发布图片
#                 for_img = list(LoseImg.objects.filter(lose=item_id).values('id', 'qiniu_img', 'lose'))
#
#                 for_all['id'] = item_id
#                 for_all['for_text'] = for_text
#                 for_all['for_img'] = for_img
#
#                 all_list.append(copy.deepcopy(for_all))
#                 # print(for_all)
#
#             data['code'] = 200
#             data['show_list'] = all_list
#
#             return JsonResponse(data)
#         else:
#             return JsonResponse({'errmsg': '尚未选择学校'})
#     else:
#         return JsonResponse({'errmsg':'请求发生错误'})


#热门活动
@require_GET
def lose_test(request):

    school_id = request.GET.get('school_id')
    if school_id:
        # 一对多 反查外键
        # 先查询 所有id
        loses_first = Lose.objects.filter(school=school_id, is_first=0).values('id', 'content').order_by('-id')

        data = {}

        data['code'] = 200
        data['loses_first'] = list(loses_first)

        return JsonResponse(data)
    else:
        return JsonResponse({'errmsg': '尚未选择学校'})








