
from django.http import JsonResponse
from django.views.decorators.http import require_POST,require_GET
from django.views.generic import View
from django.db.models import Count, F

from utils.qiniu_upload import qi_local_upload
from pro_wait.settings import MEDIA_ROOT

from second.models import Second, SecondImg, SecondComment, SecondReplyComment, SecondReport, RefuseSecond
from user.models import User, School
from moment.models import Push

import copy

# Create your views here.


# 校园二手 列表
@require_GET
def second_list(request):
    pass


# 添加 发布 校园二手
@require_POST
def second_add(request):
    pass


# 类视图方式写
# 校园二手 列表
class IndexView(View):
    def get(self, request):
        school_id = request.GET.get('school_id')
        skip = int(request.GET.get('skip'))

        # 查看是否有屏蔽说说现象   # 区别安卓 安卓这两个没有参数user_id
        refuse_two_id_list = []
        if request.GET.get('user_id'):
            user_id = request.GET.get('user_id')
            refuse_two_id = list(RefuseSecond.objects.filter(user=user_id).values('second'))
            for re in refuse_two_id:
                refuse_two_id_list.append(re['second'])

        if school_id:
            # 一对多 反查外键
            # 先查询 所有id
            end_skip = skip + 10
            seconds_list = Second.objects.filter(school=school_id, is_show=0).values('id').order_by('-id')[skip:end_skip]

            data = {}
            for_all = {}  # 单次数据
            all_list = []  # 总数据

            # 遍历id
            for item in list(seconds_list):
                # print(item.get('id'))  # {'id': 43}
                item_id = item.get('id')
                if item_id in refuse_two_id_list:
                    # 跳过此说说
                    continue
                else:
                    # 查发布内容
                    for_t = Second.objects.filter(id=item_id).values(
                        'id', 'content', 'good_num', 'create_date','create_time','price','is_type', 'view_num',
                        u_nick=F('creator__nick'),u_img=F('creator__head_qn_url'),u_id=F('creator__id'), u_token=F('creator__token')
                    ).order_by('-id')

                    for_text = list(for_t)
                    # 查发布图片
                    for_img = list(SecondImg.objects.filter(second=item_id).values('id', 'qiniu_img', 'second'))

                    for_all['id'] = item_id
                    for_all['for_text'] = for_text
                    for_all['for_img'] = for_img

                    all_list.append(copy.deepcopy(for_all))

            data['code'] = 200
            data['text_list'] = all_list

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 校园二手 添加 发布
class AddView(View):
    def post(self, request):
        # 获取ajax数据
        school_id = request.POST.get('school_id')
        creator_id = request.POST.get('creator_id')
        content = request.POST.get('content')
        price = int(request.POST.get('price'))
        is_type = int(request.POST.get('is_type'))

        # 获取ajax图片
        img_list = request.FILES.getlist('img_list')

        if school_id and creator_id:
            # 保存文本数据
            user_ins = User.objects.get(id=creator_id)
            school_ins = School.objects.get(id=school_id)
            second_create = Second.objects.create(content=content, is_type=is_type, price=price,
                                              school=school_ins, creator=user_ins)

            # 保存 外键的 图片数据
            # 这一块 写的 绝望  这次再看看 还好 总感觉不是最优写法
            if img_list and second_create:
                for img in img_list:
                    # 先保存到本地 不保存七牛 因为直接用七牛的put_data提示报错 期望不是InMemoryUploadedFile类型
                    # 不怕图片名称重复 django处理了
                    save_img = SecondImg.objects.create(local_img=img, second=second_create)

                    # 下面做七牛保存
                    second_local_img = str(MEDIA_ROOT) + '/' + str(save_img.local_img)  # 拼接本地绝对路径
                    second_img_id = save_img.id  # 获取当前本地图片的id
                    qi_local_img = qi_local_upload(second_local_img)  # 七牛上传
                    SecondImg.objects.filter(id=second_img_id).update(qiniu_img=qi_local_img)  # 更新七牛数据

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 校园二手 详情
class SecondDetailView(View):
    def get(self,request):
        second_id = request.GET.get('second_id')
        user_id = request.GET.get('user_id')

        if second_id:
            # 浏览 +1
            look_this = Second.objects.get(id=second_id)
            view_num = look_this.view_num + 1
            Second.objects.filter(id=second_id).update(view_num=view_num)

            # ======================================二手详情================================
            # 查询 详情和评论
            second = Second.objects.filter(id=second_id).values(
                'id',
                'content',
                'price',
                'view_num',
                'want_num',
                'report_num',
                'create_date',
                'create_time',
                'is_first',
                'is_type',
                'is_sale',
                c_id=F('creator__id'),
                c_nick=F('creator__nick'),
                c_head=F('creator__head_qn_url')
            )

            # 查发布图片
            img = list(SecondImg.objects.filter(second=second_id).values('id', 'qiniu_img', 'second'))

            # ======================================二手· 留言================================
            # 二手id 用户id  ---->  用户昵称，用户头像, 评论id，评论内容,排序
            comment = SecondComment.objects.filter(second=second_id).values(
                'id',
                'user',
                'content',
                'comment_date',
                'replay_num',
                c_id=F('user__id'),
                c_nick=F('user__nick'),
                c_head=F('user__head_qn_url')
            ).order_by('-id')

            data = {}
            # 将每个二级评论添加到对应的一级评论上
            for item in list(comment):
                # 获取一级评论id
                comment_id = item.get('id')
                one_replay = SecondReplyComment.objects.filter(comment=comment_id).values(
                    'id',
                    'content',
                    p_nick=F('parent__user__nick'),
                    c_nick=F('user__nick'),
                    c_id=F('user__id')
                ).order_by('id')

                # 字典
                item['replycomment'] = list(one_replay)

            data['code'] = 200
            data['img']=list(img)
            data['second_data'] = list(second)
            data['comment_data'] = list(comment)

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '请求发生错误'})


# 校园二手 添加 一级评论
class AddCommentView(View):
    def post(self, request):
        second_id = request.POST.get('second_id')
        user_id = request.POST.get('user_id')
        content = request.POST.get('content')

        if second_id and user_id:
            # 对象实例
            user_ins= User.objects.get(id=user_id)
            second_ins = Second.objects.get(id=second_id)
            SecondComment.objects.create(content=content, user=user_ins, second=second_ins )

            # 发布该二手的人的id 2019/2/24
            publisher_id = second_ins.creator_id
            # 保存信息到推送表里 2019/2/24
            Push.objects.create(push_content=content, push_type=2, publish_id=second_id, publisher_id=publisher_id,
                                commentator=user_ins)

            return JsonResponse({'msg':'数据未保存成功！'})
        else:
            return JsonResponse({'msg': '数据未保存成功！'})


# 校园二手 添加 二级评论
class ReplyCommentView(View):
    def post(self,request):
        comment_id = request.POST.get('comment_id')
        commentator_id = request.POST.get('user_id')
        second_id = request.POST.get('second_id')
        reply_id = request.POST.get('reply_id')
        reply_content = request.POST.get('reply_content')

        user_ins = User.objects.get(id=commentator_id)
        comment_ins = SecondComment.objects.get(id=comment_id)
        second_ins = Second.objects.get(id=second_id)

        # 如果是 回复的回复
        if reply_id :

            comment_reply_ins = SecondReplyComment.objects.get(id=reply_id)
            reply_comment = SecondReplyComment.objects.create(content=reply_content, user=user_ins, second=second_ins,
                                                        comment=comment_ins,parent=comment_reply_ins)
        else:
            reply_comment = SecondReplyComment.objects.create(content=reply_content,user=user_ins,second=second_ins,comment=comment_ins)

        if reply_comment:
            # 回复数量+1
            comment = SecondComment.objects.get(id=comment_id)
            replay_num = comment.replay_num + 1
            SecondComment.objects.filter(id=comment_id).update(replay_num=replay_num)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '数据没有保存成功！'})


# 校园二手 举报
class SecondReportView(View):
    def get(self, request):
        second_id = request.GET.get('second_id')
        u_id = request.GET.get('u_id')

        if second_id and u_id:
            # is_have = SecondReport.objects.filter(second=second_id,user=u_id).exists()
            # # 是否存在
            # if is_have :
            #     return JsonResponse({'msg': '已经举报过了'})

            # 举报 入表
            user_ins = User.objects.get(id=u_id)
            second_ins = Second.objects.get(id=second_id)
            SecondReport.objects.create(second=second_ins,user=user_ins)
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'msg': '已经举报过了'})


# 屏蔽此条二手
class RefuseSecondView(View):
    def get(self, request):
        second_id = request.GET.get('second_id')
        u_id = request.GET.get('u_id')

        if second_id and u_id:
            # 屏蔽此条说说 入表
            user_ins = User.objects.get(id=u_id)
            second_ins = Second.objects.get(id=second_id)
            RefuseSecond.objects.create(second=second_ins,user=user_ins)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '屏蔽失败'})