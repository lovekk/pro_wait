
from django.http import JsonResponse
from django.views.decorators.http import require_POST,require_GET
from django.views.generic import View
from django.db.models import Count, F

from utils.qiniu_upload import qi_local_upload, qi_upload
from pro_wait.settings import MEDIA_ROOT

from moment.models import Moment, Video, Image, Voice, Tag, Comment, ReplyComment, Good
from user.models import User, School, Follow

import copy

# Create your views here.


# 发现 列表
@require_GET
def moment_list(request):
    pass


# 添加 发布 发现
@require_POST
def moment_add(request):
    pass


# 类视图方式写
# 校园二手 列表
# class IndexView(View):
#     def get(self, request):
#         school_id = request.GET.get('school_id')
#         if school_id:
#             # 一对多 反查外键
#             # 先查询 所有id
#             seconds_list = Second.objects.filter(school=school_id, is_first=0).values('id', 'content','price',
#                 'good_num', 'create_date', 'create_time', 'is_type', u_nick=F('creator__nick'),
#                 u_img=F('creator__head_image'), u_id=F('creator__id'), u_token=F('creator__token')).order_by('-id')
#
#             data = {}
#             for_all = {}  # 单次数据
#             all_list = []  # 总数据
#
#             # 遍历id
#             for item in list(seconds_list):
#                 # print(item.get('id'))  # {'id': 43}
#                 item_id = item.get('id')
#                 # 查发布图片
#                 for_all['for_img'] = list(SecondImg.objects.filter(second=item_id).values('id', 'qiniu_img', 'second'))
#                 all_list.append(copy.deepcopy(for_all))
#                 # print(for_all)
#
#             data['code'] = 200
#             data['text_list'] = list(seconds_list)
#             data['img_list'] = all_list
#
#             return JsonResponse(data)
#         else:
#             return JsonResponse({'errmsg': '尚未选择学校'})


# 添加 发布
class AddView(View):
    def post(self, request):
        # 获取ajax数据
        school_id = request.POST.get('school_id')
        creator_id = request.POST.get('creator_id')
        content = request.POST.get('content')
        tag = request.POST.get('tag')

        voice_time = request.POST.get('voice_time')    # 语音时长 S
        video_size = request.POST.get('video_size')    # 视频大小 M

        # 获取ajax图片
        img_list = request.FILES.getlist('img_list')
        voice_one = request.FILES.get('voice_url')
        video_one = request.FILES.get('video_url')

        print(school_id)
        print(creator_id)
        print(content)
        print(tag)
        print(img_list)
        print(voice_one)
        print(video_one)
        print(voice_time)
        print(video_size)

        if school_id and creator_id:
            # 保存文本数据
            user_ins = User.objects.get(id=creator_id)
            school_ins = School.objects.get(id=school_id)
            moment_create = Moment.objects.create(content=content, tag=tag, school=school_ins, user=user_ins)

            # 保存 外键的 图片数据
            # 这一块 写的 绝望  这次再看看 还好 总感觉不是最优写法
            if img_list and moment_create:
                for img in img_list:
                    # 先保存到本地 不保存七牛 因为直接用七牛的put_data提示报错 期望不是InMemoryUploadedFile类型
                    # 不怕图片名称重复 django处理了
                    save_img = Image.objects.create(local_img=img, moment=moment_create)

                    # 下面做七牛保存
                    moment_local_img = str(MEDIA_ROOT) + '/' + str(save_img.local_img)  # 拼接本地绝对路径
                    moment_img_id = save_img.id  # 获取当前本地图片的id
                    qi_local_img = qi_local_upload(moment_local_img)  # 七牛上传
                    Image.objects.filter(id=moment_img_id).update(qiniu_img=qi_local_img)  # 更新七牛数据


            # 保存 外键音频
            if voice_one and moment_create:
                # django 文件上传
                save_voice = Voice.objects.create(local_voice=voice_one, voice_time=voice_time, moment=moment_create)

                # 下面做七牛保存录音
                moment_voice_one = str(MEDIA_ROOT) + '/' + str(save_voice.local_voice)  # 拼接本地绝对路径
                moment_voice_id = save_voice.id  # 获取当前本地图片的id
                qi_local_voice = qi_local_upload(moment_voice_one)  # 上传本地录音到七牛服务器
                Voice.objects.filter(id=moment_voice_id).update(qiniu_voice=qi_local_voice)  # 更新七牛数据


            # 保存 外键视频
            if video_one and moment_create:
                # django 文件上传
                save_video = Video.objects.create(local_video=video_one, video_size=video_size, moment=moment_create)

                # 下面做七牛保存视频
                moment_video_one = str(MEDIA_ROOT) + '/' + str(save_video.local_video)  # 拼接本地绝对路径
                moment_video_id = save_video.id  # 获取当前本地图片的id
                qi_local_video = qi_local_upload(moment_video_one)  # 上传本地视频到七牛服务器
                Video.objects.filter(id=moment_video_id).update(qiniu_video=qi_local_video)  # 更新七牛数据

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 获取话题标签
class TagView(View):
    def get(self, request):
        tag_list = Tag.objects.values('name')
        data = {}
        data['code'] = 200
        data['tag'] = list(tag_list)
        return JsonResponse(data)




