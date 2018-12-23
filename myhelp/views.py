from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Count, F

from user.models import User, School
from myhelp.models import Help, HelpOrder, HelpImage, HelpReport, HelpComment

from utils.qiniu_upload import qi_local_upload, qi_upload
from pro_wait.settings import MEDIA_ROOT

import copy


# help列表
class HelpListView(View):
    def get(self, request):
        school_id = request.GET.get('school_id')
        if school_id:
            # 一对多 反查外键
            # 先查询 所有id
            myhelp = Help.objects.filter(school=school_id).values('id').order_by('-id')

            data = {}
            for_one = {}  # 单次数据
            all_list = []  # 总数据

            # 遍历id
            for item in list(myhelp):
                # print(item.get('id'))  # {'id': 43}
                item_id = item.get('id')
                # 查发布内容
                for_t = Help.objects.filter(id=item_id, is_show=0).values(
                    'id', 'content', 'publish_date', 'publish_time','price','is_online','is_all_school','is_show','status',
                    u_nick=F('user__nick'), u_img=F('user__head_image'), u_id=F('user__id'))

                for_text = list(for_t)

                # 查发布图片
                for_img = list(HelpImage.objects.filter(myhelp=item_id).values('id', 'qiniu_img', 'myhelp'))

                for_one['id'] = item_id
                for_one['for_text'] = for_text
                for_one['for_img'] = for_img

                all_list.append(copy.deepcopy(for_one))
                print(for_one)

            data['code'] = 200
            data['all_list'] = all_list

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 添加help
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

                print('====================================================')
                print(content)
                print(price)
                print(is_online)
                print(is_all_school)

                school = School.objects.get(id=school_id)
                # 判断积分是否比价格大
                if user.integral >= price:
                    # 剩余积分更新
                    left_integral = user.integral - price
                    User.objects.filter(id=user_id).update(integral=left_integral)
                    # 保存数据
                    help_create = Help.objects.create(content=content,price=price,is_online=is_online,is_all_school=is_all_school,user=user,school=school)
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


# 接单
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


# 完成交易
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



# 发现 举报
class HelpReportView(View):
    def get(self, request):
        help_id = request.GET.get('help_id')
        u_id = request.GET.get('u_id')

        if help_id and u_id:
            is_have = HelpReport.objects.filter(myhelp=help_id,user=u_id).exists()

            if is_have :
                return JsonResponse({'msg': '已经举报过了'})
            else:
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
            return JsonResponse({'errmsg': '尚未选择学校'})



