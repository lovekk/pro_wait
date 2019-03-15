from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Count, F

from user.models import User, School
from moment.models import Push
from myhelp.models import Help, HelpOrder, HelpImage, HelpReport, HelpComment, HelpReplyComment, HelpCommentImage

from utils.qiniu_upload import qi_local_upload, qi_upload
from pro_wait.settings import MEDIA_ROOT
import copy


# help列表
class HelpListView(View):
    def get(self, request):
        school_id = request.GET.get('school_id')
        skip = int(request.GET.get('skip')) # 分页
        end_skip = skip + 10

        if school_id:
            # 一对多 反查外键
            # 先查询 所有id
            myhelp = Help.objects.filter(school=school_id, is_show=0).values('id').order_by('-id')[skip:end_skip]

            data = {}
            for_one = {}  # 单次数据
            all_list = []  # 总数据
            # 遍历id
            for item in list(myhelp):
                item_id = item.get('id')
                # 查发布内容
                for_t = Help.objects.filter(id=item_id).values(
                    'id', 'content', 'publish_date', 'publish_time','price','is_online','is_all_school','is_show','status',
                    u_nick=F('user__nick'), u_img=F('user__head_qn_url'), u_id=F('user__id'))

                for_text = list(for_t)
                # 查发布图片
                for_img = list(HelpImage.objects.filter(myhelp=item_id).values('id', 'qiniu_img', 'myhelp'))

                for_one['id'] = item_id
                for_one['for_text'] = for_text
                for_one['for_img'] = for_img
                all_list.append(copy.deepcopy(for_one))

            data['code'] = 200
            data['all_list'] = all_list

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 我的 help列表
class MyHelpListView(View):
    def get(self, request):
        my_id = request.GET.get('my_id')
        skip = int(request.GET.get('skip')) # 分页
        end_skip = skip + 10

        if my_id:
            # 一对多 反查外键
            # 先查询 所有id
            help_num = User.objects.get(id=my_id).help_total
            myhelp = Help.objects.filter(user=my_id, is_show=0).values('id').order_by('-id')[skip:end_skip]

            data = {}
            for_one = {}  # 单次数据
            all_list = []  # 总数据
            # 遍历id
            for item in list(myhelp):
                item_id = item.get('id')
                # 查发布内容
                for_t = Help.objects.filter(id=item_id).values(
                    'id', 'content', 'publish_date', 'publish_time','price','is_online','is_all_school','is_show','status',
                    u_nick=F('user__nick'), u_img=F('user__head_qn_url'), u_id=F('user__id'))

                for_text = list(for_t)
                # 查发布图片
                for_img = list(HelpImage.objects.filter(myhelp=item_id).values('id', 'qiniu_img', 'myhelp'))

                for_one['id'] = item_id
                for_one['for_text'] = for_text
                for_one['for_img'] = for_img
                all_list.append(copy.deepcopy(for_one))

            data['code'] = 200
            data['help_total'] = help_num
            data['all_list'] = all_list

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# help删除，从我的帮助页面删除
class DelHelp(View):
    def get(self, request):
        help_id = request.GET.get('help_id')
        user_id = request.GET.get('user_id')

        is_show = Help.objects.filter(id=help_id, user=user_id, is_show=0).exists()
        if is_show:
            # 删除 假删 修改状态而已
            Help.objects.filter(id=help_id, is_show=0).update(is_show=1)
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'msg': '抱歉，删除失败！'})


# 添加help
# ========================学生认证 积分 版 === 不用============================
class HelpAddView(View):
    def post(self,request):

        school_id = request.POST.get('school_id')
        user_id = request.POST.get('user_id')

        if school_id and user_id:
            user = User.objects.get(id=user_id)

            # 判断是否学生认证
            if user.is_school_auth == 1:
                content = request.POST.get('content')
                price = int(request.POST.get('price'))
                is_online = request.POST.get('is_type')
                is_all_school = request.POST.get('is_all_school')

                img_list = request.FILES.getlist('img_list')

                school = School.objects.get(id=school_id)
                # 判断积分是否比价格大
                if user.integral >= price:
                    # 剩余积分更新
                    left_integral = user.integral - price
                    User.objects.filter(id=user_id).update(integral=left_integral)
                    # 保存数据
                    help_create = Help.objects.create(content=content,price=price,is_online=is_online,
                                                      is_all_school=is_all_school,user=user,school=school)
                else:
                    return JsonResponse({'errmsg': '积分不足，请充值！'})

                if img_list and help_create:
                    for img in img_list:
                        # 先保存到本地 不保存七牛 因为直接用七牛的put_data提示报错 期望不是InMemoryUploadedFile类型
                        # 不怕图片名称重复 django处理了
                        save_img = HelpImage.objects.create(local_img=img, myhelp=help_create)

                        # 下面做七牛保存
                        myhelp_local_img = str(MEDIA_ROOT) + '/' + str(save_img.local_img)  # 拼接本地绝对路径
                        myhelp_img_id = save_img.id  # 获取当前本地图片的id
                        qi_local_img = qi_local_upload(myhelp_local_img)  # 七牛上传
                        HelpImage.objects.filter(id=myhelp_img_id).update(qiniu_img=qi_local_img)  # 更新七牛数据

                return JsonResponse({'code': 200})
            else:
                return JsonResponse({'errmsg': '该学生未认证，不能发布'})
        else:
            return JsonResponse({'errmsg': '尚未选择学校或该用户不存在'})


# 添加help
# ========================注册用户即可发布  暂时用这个添加help============================
class AddHelpView(View):
    def post(self,request):
        school_id = request.POST.get('school_id')
        user_id = request.POST.get('user_id')

        if school_id and user_id:
            content = request.POST.get('content')
            price = int(request.POST.get('price'))
            is_online = request.POST.get('is_type')
            is_all_school = request.POST.get('is_all_school')
            img_list = request.FILES.getlist('img_list')

            user = User.objects.get(id=user_id)
            school = School.objects.get(id=school_id)
            # 保存数据
            help_create = Help.objects.create(content=content,price=price,is_online=is_online,
                                                      is_all_school=is_all_school,user=user,school=school)
            # 说说发表数量 +1
            help_total = user.help_total + 1
            # 用户增加 2积分
            integral = user.integral + 2
            User.objects.filter(id=user_id).update(help_total=help_total,integral=integral)

            if help_create:
                for img in img_list:
                    # 先保存到本地 不保存七牛 因为直接用七牛的put_data提示报错 期望不是InMemoryUploadedFile类型
                    # 不怕图片名称重复 django处理了
                    save_img = HelpImage.objects.create(local_img=img, myhelp=help_create)

                    # 下面做七牛保存
                    myhelp_local_img = str(MEDIA_ROOT) + '/' + str(save_img.local_img)  # 拼接本地绝对路径
                    myhelp_img_id = save_img.id  # 获取当前本地图片的id
                    qi_local_img = qi_local_upload(myhelp_local_img)  # 七牛上传
                    HelpImage.objects.filter(id=myhelp_img_id).update(qiniu_img=qi_local_img)  # 更新七牛数据

                return JsonResponse({'code': 200})
            else:
                return JsonResponse({'errmsg': '未能保存图片'})
        else:
            return JsonResponse({'errmsg': '尚未选择学校或该用户不存在'})


# 帮助 help接单
class ToHelpView(View):
    def post(self,request):
        # 接收参数
        helper_id = request.POST.get('helper_id')
        help_id = request.POST.get('help_id')
        # 都存在
        if helper_id and help_id:
            # 将订单状态改成已接单
            help_ins = Help.objects.get(id=help_id)
            helper_ins = User.objects.get(id=helper_id)
            if help_ins.status == 0:

                # 创建接单信息
                order_create = HelpOrder.objects.create(is_you=0,user=helper_ins, myhelp=help_ins)

                if order_create:
                    Help.objects.filter(id=help_id).update(status=1)  # 更新为接单
                    # 用户增加 1积分
                    integral = helper_ins.integral + 1
                    User.objects.filter(id=helper_id).update(integral=integral)

                    return JsonResponse({'code': 200})
            else:
                return JsonResponse({'errmsg': '对不起，此单已被接！'})
        else:
            return JsonResponse({'errmsg':'对不起，参数出现错误！'})


# 帮助 help接单，这是认证版本，不用
class HelpOrderView(View):
    def post(self,request):
        # 接收参数
        helper_id = request.POST.get('helper_id')
        help_id = request.POST.get('help_id')
        # 都存在
        if helper_id and help_id:
            # 接单人
            helper_ins = User.objects.get(id=helper_id)
            help_ins = Help.objects.get(id=help_id)
            # 判断是否学生认证
            if helper_ins.is_school_auth == 1:
                # 将订单状态改成已接单
                Help.objects.filter(id=help_id).update(status=1)
                # 创建接单信息
                HelpOrder_create = HelpOrder.objects.create(user=helper_ins, myhelp=help_ins)

                if HelpOrder_create:
                    return JsonResponse({'code': 200})
            else:
                return JsonResponse({'errmsg': '该用户没有学生认证，不能help'})
        else:
            return JsonResponse({'errmsg':'该用户不存在'})


# 完成交易, 暂不用
class HelpFinishView(View):
    def post(self,request):
        helper_id = request.POST.get('helper_id')
        help_id = request.POST.get('help_id')
        if help_id:
            # 将订单状态改成完成状态
            Help.objects.filter(id=help_id).update(status=2)

            # 更新接单者积分
            helper = User.objects.get(id=helper_id)
            help = User.objects.get(id=help_id)
            integral = helper.integral + help.price
            User.objects.filter(id=helper_id).update(integral=integral)

        else:
            return JsonResponse({'errmsg':'未查到该help内容，或者还用户不存在'})


# help详情
class HelpDetailView(View):
    def get(self, request):
        help_id = request.GET.get('help_id')
        u_id = request.GET.get('u_id')

        if help_id:
            # 浏览 +1
            look_this = Help.objects.get(id=help_id)
            view_num = look_this.view_num + 1
            Help.objects.filter(id=help_id).update(view_num=view_num)
            # ======================================Help详情================================
            # 查询 详情和评论
            myhelp = Help.objects.filter(id=help_id).values(
                'id',
                'content',
                'publish_date',
                'publish_time',
                'price',
                'status',
                'view_num',
                'is_online',
                'is_all_school',
                'is_show',
                c_id=F('user__id'),
                c_nick=F('user__nick'),
                c_head=F('user__head_qn_url')
            )
            # 查发布图片
            img = HelpImage.objects.filter(myhelp=help_id).values('id', 'qiniu_img', 'myhelp')

            # 接单者
            if look_this.status == 1:
                helper_obj = list(HelpOrder.objects.filter(myhelp=help_id).values(
                    'order_date',
                    'order_time',
                    helper_id=F('user__id'),
                    helper_nick=F('user__nick'),
                    helper_head=F('user__head_qn_url')
                ))
            else:
                helper_obj = ''

            # ======================================Help·评论================================
            # help id 用户id  ---->  用户昵称，用户头像, 评论id，评论内容,排序
            comment = HelpComment.objects.filter(myhelp=help_id).values(
                'id',
                'content',
                'comment_date',
                'comment_time',
                c_id=F('user__id'),
                c_nick=F('user__nick'),
                c_head=F('user__head_qn_url')
            ).order_by('-id')

            data = {}
            # 将每个二级评论添加到对应的一级评论上
            for item in list(comment):
                # 获取一级评论id
                for_comment_id = item.get('id')
                # 图片
                one_img = HelpCommentImage.objects.filter(comment=for_comment_id).values('qiniu_img')

                one_replay = HelpReplyComment.objects.filter(comment=for_comment_id).values(
                    'id', 'content', p_nick=F('parent__user__nick'), c_nick=F('user__nick'), u_id=F('user__id')
                ).order_by('id')[0:5]

                # 字典
                item['one_img'] = list(one_img)

                item['replycomment'] = list(one_replay)

            data['code'] = 200
            data['img'] = list(img)
            data['helper'] = helper_obj
            data['myhelp_data'] = list(myhelp)
            data['comment_data'] = list(comment)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '请求发生错误'})


# 帮助help 添加一级评论
class AddHelpCommentView(View):
    def post(self, request):
        myhelp_id = request.POST.get('help_id')
        commentator_id = request.POST.get('user_id')
        content = request.POST.get('content')
        # 获取图片
        local_image = request.FILES.getlist('img_list')

        if myhelp_id and commentator_id:

            user_ins = User.objects.get(id=commentator_id)
            myhelp_ins = Help.objects.get(id=myhelp_id)
            # 只有文本
            comment_create = HelpComment.objects.create(content=content, user=user_ins, myhelp=myhelp_ins)

            # 发布该help的人  2019/2/24
            publisher_id = myhelp_ins.user_id
            # 保存信息到推送表里 2019/2/24
            Push.objects.create(push_content=content, push_type=1, publish_id=myhelp_id, publisher_id=publisher_id,
                                commentator=user_ins)
            # 如果有图片
            if local_image and comment_create:
                for item in local_image:
                    comment_image = HelpCommentImage.objects.create(local_img=item, comment=comment_create)
                    # 保存 图到七牛云
                    # 获取本地保存路径
                    save_image = comment_image.local_img
                    # 拼接本地绝对路径
                    comment_image_one = str(MEDIA_ROOT) + '/' + str(save_image)
                    # 上传本地图、音到七牛服务器
                    qiniu_image = qi_local_upload(comment_image_one)
                    # 更新七牛数据
                    HelpCommentImage.objects.filter(id=comment_image.id).update(qiniu_img=qiniu_image)

            if comment_create:
                return JsonResponse({'code': 200})
            else:
                return JsonResponse({'msg': '数据未保存成功！'})
        else:
            return JsonResponse({'msg': '数据未保存成功！'})


# 帮助help 添加二级评论
class ReplyHelpCommentView(View):
    def post(self, request):
        comment_id = request.POST.get('comment_id')
        commentator_id = request.POST.get('user_id')
        myhelp_id = request.POST.get('help_id')
        reply_id = request.POST.get('reply_id')
        reply_content = request.POST.get('reply_content')

        user_ins = User.objects.get(id=commentator_id)
        comment_ins = HelpComment.objects.get(id=comment_id)
        myhelp_ins = Help.objects.get(id=myhelp_id)

        # 一级评论的人的id
        publisher_id = comment_ins.user_id

        # 如果是 回复的回复
        if reply_id:
            comment_reply_ins = HelpReplyComment.objects.get(id=reply_id)
            reply_comment = HelpReplyComment.objects.create(content=reply_content, user=user_ins, myhelp=myhelp_ins,
                                                            comment=comment_ins, parent=comment_reply_ins)
            # 做推送 2019/2/24
            comment_reply_user_id = comment_reply_ins.user_id
            # 保存信息到推送表里 三级评论 2019/2/24
            Push.objects.create(push_content=reply_content, push_type=1, publish_id=myhelp_id,
                                publisher_id=comment_reply_user_id, commentator=user_ins)

        else:
            reply_comment = HelpReplyComment.objects.create(content=reply_content, user=user_ins, myhelp=myhelp_ins,
                                                            comment=comment_ins)
            # 保存信息到推送表里 二级评论 2019/2/24
            Push.objects.create(push_content=reply_content, push_type=1, publish_id=myhelp_id,
                                publisher_id=publisher_id, commentator=user_ins)

        if reply_comment:

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '数据没有保存成功！'})


# 帮助help 举报
class HelpReportView(View):
    def get(self, request):
        help_id = request.GET.get('help_id')
        u_id = request.GET.get('u_id')

        if help_id and u_id:
            # 不做判断 耗性能
            # is_have = HelpReport.objects.filter(myhelp=help_id,user=u_id).exists()
            # if is_have :
            #     return JsonResponse({'msg': '已经举报过了'})

            # 举报 +1
            report_this = Help.objects.get(id=help_id)
            report_num = report_this.report_num + 1
            Help.objects.filter(id=help_id).update(report_num=report_num)

            # 举报 入表
            user_ins = User.objects.get(id=u_id)
            help_ins = Help.objects.get(id=help_id)
            HelpReport.objects.create(myhelp=help_ins,user=user_ins)

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'msg': '已经举报过了！'})


# ===============================统计======我发布的=====我接单的==========================
# Help订单
# 1.我发布的
class PublishOrderView(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if user_id:
            help = Help.objects.filter(user=user_id).values(
                'content',
                'publish_date',
                'price',
                'is_online',
                'is_allschool',
                c_head=F('order__user__head_qn_url'),
                c_nick=F('order__user__nick'),
                school=F('order__school__name'),
                status=F('order__status'),
                order_datetime=F('order__order_datetime'),
                finished_datetime=F('order__finished_datetime')
            ).order_by('-publish_date')

            data = {}
            data['code'] = 200
            data['my_publish'] = list(help)
        else:
            return JsonResponse({'errmsg': '用户不存在'})


# 1.我接单的
class TakeOrderView(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if user_id:
            order = HelpOrder.objects.filter(user=user_id)
            help = Help.objects.filter(order=order).values(
                'content',
                'publish_date',
                'price',
                'is_online',
                'is_allschool',
                c_id=F('user__id'),
                c_head=F('user__head_qn_url'),
                c_nick=F('user__nick'),
                school=F('school__name'),
                status=F('order__status'),
                order_datetime=F('order__order_datetime'),
                finished_datetime=F('order__finished_datetime')
            ).order_by('-publish_date')

            data = {}
            data['code'] = 200
            data['my_take'] = list(help)
        else:
            return JsonResponse({'errmsg': '用户不存在'})




