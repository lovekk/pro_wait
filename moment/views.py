from django.http import JsonResponse
from django.views.decorators.http import require_POST,require_GET
from django.views.generic import View
from django.db.models import Count, F

from utils.qiniu_upload import qi_local_upload, qi_upload
from pro_wait.settings import MEDIA_ROOT
import copy

from moment.models import Moment, Video, Image, Voice, Tag, Good, Report, Push, RefuseFind, RefuseUser
from moment.models import Comment, ReplyComment, CommentGood, CommentImage, CommentVideo, CommentVoice
from user.models import User, School, Follow

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
# =================================================发现===========================================
# 说说 首页 列表
class IndexView(View):
    def get(self, request):
        school_id = request.GET.get('school_id')
        user_id = request.GET.get('user_id')
        choose_one = int(request.GET.get('choose_one')) # 0-最新 1-热门 2-关注
        skip = int(request.GET.get('skip')) # 分页

        if school_id:
            # 一对多 反查外键  先查询 所有id
            moments_first = []
            end_skip = skip + 10

            # 查看是否有屏蔽说说现象
            refuse_find_id_list = []
            refuse_find_id = list(RefuseFind.objects.filter(user=user_id).values('moment'))
            for re in refuse_find_id:
                refuse_find_id_list.append(re['moment'])

            # 查看是否屏蔽用户
            refuse_user_id_list = []
            refuse_user_id = list(RefuseUser.objects.filter(my_id=user_id).values('his_id'))
            for re in refuse_user_id:
                refuse_user_id_list.append(re['his_id'])


            # 最新
            if choose_one == 0:
                # moments_first = Moment.objects.filter(school=school_id, is_first=0, is_show=0 ).values('id').order_by('-id')
                moments_first = Moment.objects.filter(school=school_id, is_first=0, is_show=0).exclude(user__in=refuse_user_id_list).values('id').order_by('-id')[skip:end_skip]
            # 热门
            if choose_one == 1:
                moments_first = Moment.objects.filter(school=school_id, is_show=0, comment_num__gt=5).exclude(user__in=refuse_user_id_list).values('id').order_by('-id')[skip:end_skip]
            # 关注
            if choose_one == 2:
                user = User.objects.get(id=user_id)
                follow_u_id = []
                follows = list(user.follow_set.filter(is_delete=0).values('follow_id'))
                for item in follows:
                    one_id = item['follow_id']
                    follow_u_id.append(one_id)
                moments_first = Moment.objects.filter(user__in=follow_u_id, is_show=0).exclude(tag='匿名树洞',user__in=refuse_user_id_list).values('id').order_by('-publish_date','-id')[skip:end_skip]

            data = {}
            for_one = {}  # 单次数据
            all_list = []  # 总数据

            # 遍历id
            for item in list(moments_first):
                item_id = item.get('id')
                if item_id in refuse_find_id_list:
                    # 跳过此说说
                    continue
                else:
                    # 浏览 +1
                    look_this = Moment.objects.get(id=item_id)
                    view_num = look_this.view_num + 1
                    Moment.objects.filter(id=item_id).update(view_num=view_num)

                    # 查发布内容
                    for_t = Moment.objects.filter(id=item_id).values(
                        'id', 'content', 'good_num', 'publish_date', 'publish_time','tag','comment_num','view_num','comment_num',
                        u_nick=F('user__nick'), u_img=F('user__head_qn_url'), u_id=F('user__id'))

                    for_text = list(for_t)
                    # 查发布图片
                    for_img = list(Image.objects.filter(moment=item_id).values('id', 'qiniu_img', 'moment'))
                    # 查看 录音
                    for_voice = list(Voice.objects.filter(moment=item_id).values('id', 'qiniu_voice', 'local_voice','voice_time','moment'))
                    # 查看 视频
                    for_video = list(Video.objects.filter(moment=item_id).values('id', 'qiniu_video', 'moment'))
                    # 是否点赞
                    for_good = Good.objects.filter(moment=item_id,user=user_id).exists()

                    for_one['id'] = item_id
                    for_one['for_text'] = for_text
                    for_one['for_img'] = for_img
                    for_one['for_voice'] = for_voice
                    for_one['for_video'] = for_video
                    for_one['for_good'] = for_good
                    # 单个 追加
                    all_list.append(copy.deepcopy(for_one))

            data['code'] = 200
            data['all_list'] = all_list

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 添加 发现 add
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

        if school_id and creator_id:
            # 保存文本数据
            user_ins = User.objects.get(id=creator_id)
            school_ins = School.objects.get(id=school_id)
            moment_create = Moment.objects.create(content=content, tag=tag, school=school_ins, user=user_ins)

            find_this = User.objects.get(id=creator_id)
            # 说说发表数量 +1
            find_total = find_this.find_total + 1
            # 用户增加 1积分
            integral = find_this.integral + 1
            User.objects.filter(id=creator_id).update(find_total=find_total,integral=integral)

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


# 发现详情
class MomentDetailView(View):
    # 发现 具体内容 详情 正文
    def get(self,request):
        moment_id = request.GET.get('moment_id')
        u_id = request.GET.get('u_id')
        his_id = request.GET.get('his_id')

        if moment_id:
            # 浏览 +1
            look_this = Moment.objects.get(id=moment_id)
            view_num = look_this.view_num + 1
            Moment.objects.filter(id=moment_id).update(view_num=view_num)
            # ======================================发现详情================================
            # 查询 详情和评论
            moment = Moment.objects.filter(id=moment_id).values(
                'id',
                'content',
                'publish_date',
                'publish_time',
                'tag',
                'good_num',
                'comment_num',
                'view_num',
                'relay_num',
                c_id=F('user__id'),
                c_nick=F('user__nick'),
                c_head=F('user__head_qn_url')
            )
            # 查发布图片
            img = list(Image.objects.filter(moment=moment_id).values('id', 'qiniu_img', 'moment'))
            # 查看 音频
            voice = list(Voice.objects.filter(moment=moment_id).values('id', 'qiniu_voice','voice_time', 'moment'))
            # 查看 视频
            video = list(Video.objects.filter(moment=moment_id).values('id', 'qiniu_video', 'moment'))
            # 是否点赞
            is_good = Good.objects.filter(moment=moment_id, user=u_id).exists()
            # ======================================发现·评论================================
            # 发现id 用户id  ---->  用户昵称，用户头像, 评论id，评论内容,排序
            comment = Comment.objects.filter(moment=moment_id).values(
                'id',
                'user',
                'content',
                'comment_date',
                'comment_time',
                'good_num',
                'replay_num',
                c_id=F('user__id'),
                c_nick=F('user__nick'),
                c_head=F('user__head_qn_url')
            ).order_by('-id')

            data = {}  # 总数据
            # 将每个二级评论添加到对应的一级评论上
            for item in list(comment):
                # 获取一级评论id
                for_comment_id = item.get('id')
                # 图片
                one_img = CommentImage.objects.filter(comment=for_comment_id).values('qiniu_img')
                one_voice = CommentVoice.objects.filter(comment=for_comment_id).values('id','qiniu_voice','voice_time')
                one_video = CommentVideo.objects.filter(comment=for_comment_id).values('qiniu_video')
                one_replay = ReplyComment.objects.filter(comment=for_comment_id).values(
                    'id','content', p_nick=F('parent__user__nick'), c_nick=F('user__nick'),u_id=F('user__id')
                    ).order_by('id')[0:5]
                # 是否点赞
                one_good = CommentGood.objects.filter(comment=for_comment_id,user=u_id).exists()
                # 字典
                item['one_img'] = list(one_img)
                item['one_voice'] = list(one_voice)
                item['one_video'] = list(one_video)
                item['one_good'] = one_good
                item['replycomment'] = list(one_replay)

            data['code'] = 200
            data['img']=list(img)
            data['voice']=list(voice)
            data['video']=list(video)
            data['is_good']=is_good
            data['moment_data'] = list(moment)

            # 查看是否关注
            if his_id == u_id:
                data['follow'] = 2
            else:
                is_follow = Follow.objects.filter(follow_id=his_id, user=u_id, is_delete=0).exists()
                if is_follow:
                    # 已经关注了
                    data['follow'] = 1
                else:
                    data['follow'] = 0  #没有关注

            data['comment_data'] = list(comment)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '请求发生错误'})


# 发现 删除，从我的个人主页删除
class DelMoment(View):
    def get(self, request):
        moment_id = request.GET.get('moment_id')
        user_id = request.GET.get('user_id')

        is_show = Moment.objects.filter(id=moment_id, user=user_id, is_show=0).exists()
        if is_show:
            # 删除 假删 修改状态而已
            Moment.objects.filter(id=moment_id).update(is_show=1)
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'msg': '抱歉，删除失败！'})


# 发现 点赞
class MomentGoodView(View):
    def get(self, request):
        moment_id = request.GET.get('moment_id')
        u_id = request.GET.get('u_id')
        his_id = request.GET.get('his_id')

        if moment_id and u_id:
            # 其实不用判断是否已经点赞
            # is_good = Good.objects.filter(moment=moment_id, user=u_id).exists()
            # if is_good:
            #     return JsonResponse({'msg': '已经点赞'})

            # 本说说点赞 +1
            good_this = Moment.objects.get(id=moment_id)
            good_num = good_this.good_num + 1
            Moment.objects.filter(id=moment_id).update(good_num=good_num)

            # 个人点赞总数
            his_ins = User.objects.get(id=his_id)
            good_total = his_ins.good_total + 1
            User.objects.filter(id=his_id).update(good_total=good_total)

            # 点赞入表
            user_ins = User.objects.get(id=u_id)
            moment_ins = Moment.objects.get(id=moment_id)
            Good.objects.create(moment=moment_ins, user=user_ins)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'msg': '尚未选择学校'})


# 发现 举报
class ReportView(View):
    def get(self, request):
        moment_id = request.GET.get('moment_id')
        u_id = request.GET.get('u_id')

        if moment_id and u_id:
            # 不一定要判断，感觉效率太低
            # is_have = Report.objects.filter(moment=moment_id,user=u_id).exists()
            #
            # if is_have :
            #     return JsonResponse({'msg': '已经举报过了'})

            # 举报 +1
            report_this = Moment.objects.get(id=moment_id)
            report_num = report_this.report_num + 1
            Moment.objects.filter(id=moment_id).update(report_num=report_num)

            # 举报 入表
            user_ins = User.objects.get(id=u_id)
            moment_ins = Moment.objects.get(id=moment_id)
            Report.objects.create(moment=moment_ins,user=user_ins)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 发现 屏蔽此条说说
class RefuseFindView(View):
    def get(self, request):
        moment_id = request.GET.get('moment_id')
        u_id = request.GET.get('u_id')

        if moment_id and u_id:
            # 屏蔽此条说说 入表
            user_ins = User.objects.get(id=u_id)
            moment_ins = Moment.objects.get(id=moment_id)
            RefuseFind.objects.create(moment=moment_ins,user=user_ins)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '屏蔽失败'})


# 发现 屏蔽此用户
class RefuseUserView(View):
    def get(self, request):
        his_id = request.GET.get('his_id')
        my_id = request.GET.get('my_id')

        if his_id and my_id:
            # 屏蔽此用户 入表
            my_ins = User.objects.get(id=my_id)
            RefuseUser.objects.create(his_id=his_id,my_id=my_ins)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 屏蔽用户列表
class RefuseListView(View):
    def get(self,request):
        my_id = request.GET.get('my_id')

        if my_id:
            # 查询出所有的关注
            data = {}

            cancel_u_id = []
            # 找到所有
            follows = list(RefuseUser.objects.filter(my_id=my_id).values('his_id').order_by('-id'))
            # 追加到一个列表里面
            for item in follows:
                one_id = item['his_id']
                cancel_u_id.append(one_id)
            # 用户id 在这个列表里
            cancel_list = User.objects.filter(id__in=cancel_u_id).values('id', 'nick','head_qn_url','school_name')

            data['code'] = 200
            data['cancel_list'] = list(cancel_list)

            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg": "用户不存在"})

# 取消屏蔽
class CancelRefuseView(View):
    def get(self,request):
        his_id = request.GET.get('his_id')

        if his_id:
            RefuseUser.objects.filter(his_id=his_id).delete()
            data = {}
            data['code'] = 200

            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg": "用户不存在"})

# =================================================发现·评论===========================================
# 添加 一级评论
class AddCommentView(View):
    def post(self, request):
        moment_id = request.POST.get('moment_id')
        commentator_id = request.POST.get('user_id')
        content = request.POST.get('content')
        his_id = request.POST.get('his_id')
        # 获取图片
        local_image = request.FILES.getlist('img_list')
        # 获取音频
        local_voice = request.FILES.get('voice_url')
        voice_time = request.POST.get('voice_time')  # 语音时长 S
        # 视频
        local_video = request.FILES.get('video_url')
        video_size = request.POST.get('video_size')  # 视频大小
        if moment_id and commentator_id:
            user_ins = User.objects.get(id=commentator_id)
            moment_ins = Moment.objects.get(id=moment_id)

            # 先存到推送
            # 发布该说说的人的id 2019/2/24  他的id
            publisher_id = moment_ins.user_id
            # 保存信息到推送表里 2019/2/24
            Push.objects.create(push_content=content, push_type=0, publish_id=moment_id,
                                publisher_id=publisher_id, commentator=user_ins)

            # 只有文本
            comment_create = Comment.objects.create(content=content, user=user_ins, moment=moment_ins)
            # 如果有图片
            if local_image and comment_create:
                for item in local_image:

                    comment_image = CommentImage.objects.create(local_img=item,comment=comment_create)
                    # 保存 图到七牛云
                    # 获取本地保存路径
                    save_image = comment_image.local_img
                    # 拼接本地绝对路径
                    comment_image_one = str(MEDIA_ROOT) + '/' + str(save_image)
                    # 上传本地图、音到七牛服务器
                    qiniu_image = qi_local_upload(comment_image_one)
                    # 更新七牛数据
                    CommentImage.objects.filter(id=comment_image.id).update(qiniu_img=qiniu_image)

            # 如果有音频
            if local_voice and comment_create:
                comment_voice = CommentVoice.objects.create(local_voice=local_voice, voice_time=voice_time, comment=comment_create)

                # 保存语音到七牛云
                # 获取本地保存路径
                save_voice = comment_voice.local_voice
                # 拼接本地绝对路径
                comment_voice_one = str(MEDIA_ROOT) + '/' + str(save_voice)
                # 上传本地图、音到七牛服务器
                qiniu_voice = qi_local_upload(comment_voice_one)
                # 更新七牛数据
                comment = CommentVoice.objects.filter(id=comment_voice.id).update(qiniu_voice=qiniu_voice)

            # 如果有视频
            if local_video and comment_create:
                comment_video = CommentVideo.objects.create(local_video=local_video, video_size=video_size, comment=comment_create)

                # 保存到七牛云
                # 获取本地保存路径
                save_video = comment_video.local_video
                # 拼接本地绝对路径
                comment_video_one = str(MEDIA_ROOT) + '/' + str(save_video)
                # 上传本地图、音到七牛服务器
                qiniu_video = qi_local_upload(comment_video_one)
                # 更新七牛数据
                comment = CommentVideo.objects.filter(id=comment_video.id).update(qiniu_video=qiniu_video)

            if comment_create:
                # 评论数量+1
                moment = Moment.objects.get(id=moment_id)
                comment_num = moment.comment_num + 1
                Moment.objects.filter(id=moment_id).update(comment_num=comment_num)

                # 个人获得评论总数
                his_ins = User.objects.get(id=his_id)
                comment_total = his_ins.comment_total + 1
                User.objects.filter(id=his_id).update(comment_total=comment_total)

                return JsonResponse({'code': 200})
            else:
                return JsonResponse({'msg':'数据未保存成功！'})
        else:
            return JsonResponse({'msg': '数据未保存成功！'})


# 添加 二级评论
class ReplyCommentView(View):
    def post(self,request):
        comment_id = request.POST.get('comment_id')
        commentator_id = request.POST.get('user_id')
        moment_id = request.POST.get('moment_id')
        reply_id = request.POST.get('reply_id')
        reply_content = request.POST.get('reply_content')
        his_id = request.POST.get('his_id')

        user_ins = User.objects.get(id=commentator_id)
        comment_ins = Comment.objects.get(id=comment_id)
        moment_ins = Moment.objects.get(id=moment_id)

        # 一级评论者 接收回复的用户的id
        publisher_id = comment_ins.user_id

        # 如果是 回复的回复
        if reply_id :
            comment_reply_ins = ReplyComment.objects.get(id=reply_id)
            reply_comment = ReplyComment.objects.create(content=reply_content, user=user_ins, moment=moment_ins,
                                                        comment=comment_ins,parent=comment_reply_ins)
            # 推送 评论 入表
            # publisher_id ===》发布者，接收评论的人
            # commentator ==》这一次做评论的人
            comment_reply_user_id = comment_reply_ins.user_id
            # 保存信息到推送表里 三级评论 2019/2/24
            Push.objects.create(push_content=reply_content, push_type=0, publish_id=moment_id,
                                publisher_id=comment_reply_user_id, commentator=user_ins)
        else:
            reply_comment = ReplyComment.objects.create(content=reply_content,user=user_ins,moment=moment_ins,comment=comment_ins)
            # 保存信息到推送表里 二级评论 2019/2/24
            Push.objects.create(push_content=reply_content, push_type=0, publish_id=moment_id,
                                publisher_id=publisher_id, commentator=user_ins)

        if reply_comment:
            # 回复数量+1
            comment = Comment.objects.get(id=comment_id)
            replay_num = comment.replay_num + 1
            Comment.objects.filter(id=comment_id).update(replay_num=replay_num)

            # 评论数量+1
            moment = Moment.objects.get(id=moment_id)
            comment_num = moment.comment_num + 1
            Moment.objects.filter(id=moment_id).update(comment_num=comment_num)

            # 个人获得评论总数
            his_ins = User.objects.get(id=his_id)
            comment_total = his_ins.comment_total + 1
            User.objects.filter(id=his_id).update(comment_total=comment_total)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '数据没有保存成功！'})


#评论点赞
class CommentGoodView(View):
    def get(self, request):
        comment_id = request.GET.get('comment_id')
        u_id = request.GET.get('u_id')

        if comment_id and u_id:
            is_good = CommentGood.objects.filter(comment=comment_id, user=u_id).exists()

            if is_good:
                return JsonResponse({'msg': '已经点赞'})
            else:
                # 点赞 +1
                good_this = Comment.objects.get(id=comment_id)
                good_num = good_this.good_num + 1
                Comment.objects.filter(id=comment_id).update(good_num=good_num)

                user_ins = User.objects.get(id=u_id)
                comment_ins = Comment.objects.get(id=comment_id)
                CommentGood.objects.create(comment=comment_ins, user=user_ins)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '未接收到数据！'})


# 二级评论大于5条详情页
class ReplyCommentDetailView(View):
    def get(self,request):
        comment_id = request.GET.get('comment_id')
        if comment_id:
            comment_detail = Comment.objects.filter(id = comment_id).values('id','content','replay_num','good_num',
                'comment_date',c_head=F('user__head_qn_url'),c_nick=F('user__nick'),)
            reply_comment_list = ReplyComment.objects.filter(comment=comment_id).values(
                'content',
                'comment_date',
                c_head=F('user__head_qn_url'),
                c_nick=F('user__nick'),
            )
            data = {}
            data['code'] = 200
            data['comment_detail'] = list(comment_detail)
            data['reply_moment_data'] = list(reply_comment_list)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '未接收到comment_id'})


# =================================================发现·其他===========================================

# 获取话题标签
class TagView(View):
    def get(self, request):
        tag_list = Tag.objects.values('name')
        data = {}
        data['code'] = 200
        data['tag'] = list(tag_list)
        return JsonResponse(data)


# 添加关注
class CreateFollow(View):
    def get(self,request):
        user_id = request.GET.get('user_id')
        follow_id = request.GET.get('his_id')

        if user_id and follow_id:

            # 添加关注
            user_ins = User.objects.get(id=user_id)
            Follow.objects.create(follow_id=follow_id, user=user_ins)

            # 我关注的人的总数
            create_total = user_ins.create_total + 1
            User.objects.filter(id=user_id).update(create_total=create_total)

            # 他的粉丝
            his_ins = User.objects.get(id=follow_id)
            fans_total = his_ins.fans_total + 1
            User.objects.filter(id=follow_id).update(fans_total=fans_total)

            return JsonResponse({"code": 200})
        else:
            return JsonResponse({"errmsg": "该用户不存在"})


# 取消关注
class CancelFollow(View):
    def get(self,request):
        user_id = request.GET.get('user_id')
        follow_id = request.GET.get('his_id')

        if user_id and follow_id:
            is_follow = Follow.objects.filter(follow_id=follow_id, user=user_id, is_delete=0).exists()

            if is_follow:
                # 确实已经关注了，修改一下状态，取消关注
                Follow.objects.filter(follow_id=follow_id, user=user_id).update(is_delete=1)

                # 我关注的人的总数
                user_ins = User.objects.get(id=user_id)
                create_total = user_ins.create_total - 1
                User.objects.filter(id=user_id).update(create_total=create_total)

                # 他的粉丝
                his_ins = User.objects.get(id=follow_id)
                fans_total = his_ins.fans_total - 1
                User.objects.filter(id=follow_id).update(fans_total=fans_total)

                return JsonResponse({"code": 200})
        else:
            return JsonResponse({"errmsg": "该用户不存在"})


# 搜索功能  根据输入的关键字  查询出 1.带有关键字的用户 2.带有关键字的moment
class SearchView(View):
    def get(self,request):
        school_id = request.GET.get('school_id')
        user_id = request.GET.get('user_id')
        key_words = request.GET.get('key_words')

        if school_id and key_words and user_id:
            user = User.objects.filter(school=school_id,nick__icontains=key_words).values('id','nick','head_qn_url','school_name')
            # 一对多 反查外键
            # 先查询 所有id, 只查询前20个，不做分页了
            moments_first = Moment.objects.filter(school=school_id, is_show=0, content__icontains=key_words).values('id').order_by('-id')[0:20]

            data = {}
            for_one = {}  # 单次数据
            all_list = []  # 总数据

            # 遍历id
            for item in list(moments_first):
                item_id = item.get('id')
                # 浏览 +1
                look_this = Moment.objects.get(id=item_id)
                view_num = look_this.view_num + 1
                Moment.objects.filter(id=item_id).update(view_num=view_num)

                # 查发布内容
                for_t = Moment.objects.filter(id=item_id).values(
                    'id', 'content', 'good_num', 'publish_date', 'publish_time', 'tag', 'comment_num', 'view_num',
                    'comment_num',
                    u_nick=F('user__nick'), u_img=F('user__head_qn_url'), u_id=F('user__id'))

                for_text = list(for_t)
                # 查发布图片
                for_img = list(Image.objects.filter(moment=item_id).values('id', 'qiniu_img', 'moment'))
                # 查看 录音
                for_voice = list(
                    Voice.objects.filter(moment=item_id).values('id', 'qiniu_voice', 'local_voice', 'voice_time',
                                                                'moment'))
                # 查看 视频
                for_video = list(Video.objects.filter(moment=item_id).values('id', 'qiniu_video', 'moment'))
                # 是否点赞
                for_good = Good.objects.filter(moment=item_id, user=user_id).exists()

                for_one['id'] = item_id
                for_one['for_text'] = for_text
                for_one['for_img'] = for_img
                for_one['for_voice'] = for_voice
                for_one['for_video'] = for_video
                for_one['for_good'] = for_good
                # 单个 追加
                all_list.append(copy.deepcopy(for_one))

            data['code'] = 200
            data['user_list'] = list(user)
            data['all_list'] = all_list

            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg":"未选择学校或者未接收到关键字参数"})


# 评论推送，通知 2019/2/23
class PushView(View):
    def get(self,request):
        user_id = request.GET.get('user_id')
        skip = int(request.GET.get('skip'))
        skip_end = skip + 10
        data = {}
        if user_id:
            push = Push.objects.filter(publisher_id=user_id).values(
                'push_content',
                'push_type',
                'publish_id',
                'comment_date',
                'comment_time',
                u_id=F('commentator__id'),
                u_nick=F('commentator__nick'),
                u_school=F('commentator__school_name'),
                u_img=F('commentator__head_qn_url')
            ).order_by('-id')[skip:skip_end]

            data['code'] = 200
            data['push_data'] = list(push)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '没接收到数据！'})