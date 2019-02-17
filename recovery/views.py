from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from .models import Price, Appoint, MyRank, Bag, Introduction, Tips
from user.models import User, School,RecoveryPerson
from django.db.models import Count, F


# 添加预约
class AddAppoint(View):
    def post(self,request):
        school_id = request.POST.get('school_id')
        user_id = request.POST.get('user_id')

        if school_id and user_id:
            # 预约数据
            thing_type = request.POST.get('thing_type')
            address = request.POST.get('address')
            phone_num = request.POST.get('phone_num')
            print(phone_num)
            remark = request.POST.get('remark')

            #外键实例
            school_ins = School.objects.get(id=school_id)
            user_ins = User.objects.get(id=user_id)

            appoint_create = Appoint.objects.create(thing_type=thing_type,address=address,phone_num=phone_num,remark=remark,user=user_ins,school=school_ins)

            if appoint_create:
                return JsonResponse({'code': 200})
            else:
                return JsonResponse({'errmsg': '预约失败'})
        else:
            return JsonResponse({'errmsg':'未选择学校'})


# 上门扫码 更新预约状态
class Scan(View):
    # 1.给一个预约的id，扫码显示一个袋子编号
    def post(self,request):
        user_id = request.POST.get('user_id')
        school_id = request.POST.get('school_id')
        #  获取到袋子编号，输入传给后端保存
        bag_num = request.POST.get('bag_num')
        is_bag = Bag.objects.filter(number=bag_num).exists()
        print(bag_num)
        print(is_bag)

        if user_id and is_bag:
            # 根据用户查找出来最新的一条预约记录
            first_appoint = list(Appoint.objects.filter(user=user_id, status=0).values('id').order_by('-id')[0:1])

            if first_appoint:
                # 找出来id
                appoint_id = first_appoint[0].get('id')
                # 预约表里面 单次回收积分和袋子编号要更新
                Appoint.objects.filter(id=appoint_id).update(bag_num=bag_num, status=1)
                return JsonResponse({"code": 200})
            else:
                return JsonResponse({"errmsg": "您还没有预约！"})
        else:
            return JsonResponse({"errmsg":"您绑定的回收袋不存在！"})



#一键预约
class OneKey(View):
    def get(self,request):
        # 获取学校
        school_id = request.GET.get('school_id')
        # 数据
        data = {}
        if school_id:
            # 只有前一百名
            all_rank = MyRank.objects.filter(school=school_id).values('money','times',u_nick=F('user__nick')).order_by('-money')[0:100]
            data['code'] = 200
            data['rank'] = list(all_rank)
            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg":"没选择学校"})


#排名显示
class RankList(View):
    def get(self,request):
        # 获取学校
        school_id = request.GET.get('school_id')
        # 数据
        data = {}
        if school_id:
            # 只有前一百名
            all_rank = MyRank.objects.filter(school=school_id).values('money','times',u_nick=F('user__nick')).order_by('-money')[0:100]
            data['code'] = 200
            data['rank'] = list(all_rank)
            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg":"没选择学校"})


# 显示回收物品的价格信息
class ThingPriceList(View):
    def get(self,request):
        things = Price.objects.values()
        data = {}
        data['code'] = 200
        data['thing_msg'] = list(things)

        return JsonResponse(data)


# 预约提醒信息
class AppointTips(View):
    def get(self,request):
        school_id = request.GET.get('school_id')
        user_id = request.GET.get('user_id')
        if school_id:
            tip = Tips.objects.filter(school=school_id).values().order_by('-id')[0:1]
            # 根据用户查找出来最新的一条预约记录
            # 显示预约状态
            # 用户预约过 会显示first_appoint: [{status: 0}]
            # 用户一次都没有预约过 会显示first_appoint: []
            first_appoint = list(Appoint.objects.filter(user=user_id).values('status').order_by('-id')[0:1])

            data = {}
            data['code'] = 200
            data['tip_msg'] = list(tip)
            data['first_appoint'] = list(first_appoint)

            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg":"未选择学校"})


# 环保知识简介
class Introduce(View):
    def get(self,request):

        introduce = list(Introduction.objects.values().order_by('-id')[0:1])
        data = {}
        data['code'] = 200
        data['introduce'] = introduce

        # 找出来id
        introduce_id = introduce[0].get('id')

        # 浏览 +1
        look_this = Introduction.objects.get(id=introduce_id)
        view_num = look_this.view_num + 1
        Introduction.objects.filter(id=introduce_id).update(view_num=view_num)

        return JsonResponse(data)


# ===========================================新的APP  官方回收人员专用=============================================
# 0.找袋子的预约信息
class FindBagView(View):
    def get(self,request):
        # 1.扫描袋子，得到袋子编号,获取袋子编号
        bag_num = request.GET.get('bag_num')
        # 2.判断袋子编号是否正确，即数据库里能查到该袋子编号,
        is_have = Appoint.objects.filter(bag_num=bag_num, status=1).exists()

        print(is_have)

        if is_have:
            # 袋子存在 找出信息
            bag_msg = Appoint.objects.filter(bag_num=bag_num,status=1).values(
                'id',
                'user__id',
                'user__school',
                'user__nick',
                'thing_type',
                'address',
                'phone_num',
                'remark',
                'status',
            ).order_by('-id')[0:1]
            data = {}
            data['code'] = 200
            data['bag_msg'] = list(bag_msg)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg':'该回收袋/预约不存在'})


# 1.称重
class WeighView(View):
    def post(self,request):
        # 1.扫描袋子，得到袋子编号,获取袋子编号
        appoint_id = request.POST.get('appoint_id')
        user_id = request.POST.get('user_id')
        school_id = request.POST.get('school_id')
        bag_num = request.POST.get('bag_num')
        worker_num = request.POST.get('worker_num')

        get_money = int(request.POST.get('money'))
        get_weight = request.POST.get('weight')

        # 2.判断袋子编号是否正确，即数据库里能查到该袋子编号,
        is_have = Appoint.objects.filter(id=appoint_id, bag_num=bag_num, status=1).exists()
        # 袋子状态为“绑袋中”
        # 3.袋子编号正确，称重，算出积分 ，更新数据库
        if is_have:
            #  4.更新积分和预约状态
            Appoint.objects.filter(id=appoint_id,bag_num=bag_num, status=1).update(
                money=get_money,
                status=2,
                weight=get_weight,
                worker_num=worker_num
            )

            #我的排名表里面的积分要更新，投递次数更新
            is_my_rank = MyRank.objects.filter(user=user_id).exists()
            if is_my_rank:
                # 如果存在
                # 更新回收排行次数 排行积分
                my_rank = MyRank.objects.get(user=user_id)
                times = my_rank.times + 1
                money = my_rank.money + get_money
                MyRank.objects.filter(user=user_id).update(times=times,money=money)

                # 更新该用户总积分
                user_up = User.objects.get(id=user_id)
                print(user_up)
                print(user_up.integral)
                integral_num = user_up.integral + get_money
                User.objects.filter(id=user_id).update(integral=integral_num)

                return JsonResponse({'code': 200})
            else:
                # 不存在 就创建
                # 外键实例
                school_ins = School.objects.get(id=school_id)
                user_ins = User.objects.get(id=user_id)
                MyRank.objects.create(times=1, money=get_money, user=user_ins, school=school_ins)

                # 更新该用户总积分
                user_up = User.objects.get(id=user_id)
                print(user_up)
                print(user_up.integral)
                integral_num = user_up.integral + get_money
                User.objects.filter(id=user_id).update(integral=integral_num)

                return JsonResponse({'code': 201})
        else:
            return JsonResponse({'errmsg':'该回收袋/预约不存在'})


# 2.0 预约的订单
class PreOrderListView(View):
    def get(self,request):
        school_id = request.GET.get('school_id')
        if school_id:
            # 已经绑袋子的信息
            order_list = Appoint.objects.filter(school=school_id,status=0).values(
                'thing_type',
                'address',
                'phone_num',
                'remark',
                'create_date',
                u_phone=F('user__phone_num'),
                u_nick=F('user__nick'),
            ).order_by('-id')
            data = {}
            data['code'] = 200
            data['order_list'] = list(order_list)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '未选择学校'})


# 2.1 绑袋子的订单
class OrderListView(View):
    def get(self,request):
        school_id = request.GET.get('school_id')
        if school_id:
            # 已经绑袋子的信息
            order_list = Appoint.objects.filter(school=school_id,status=1).values(
                'thing_type',
                'address',
                'phone_num',
                'bag_num',
                'remark',
                'create_date',
                u_nick=F('user__nick'),
            ).order_by('-id')
            data = {}
            data['code'] = 200
            data['order_list'] = list(order_list)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '未选择学校'})


# 3.绑袋子的完成的历史订单
class HistoryListView(View):
    def get(self,request):
        school_id = request.GET.get('school_id')
        if school_id:
            # 已经绑袋子的信息
            history_list = Appoint.objects.filter(school=school_id,status=2).values(
                'thing_type',
                'weight',
                'money',
                'bag_num',
                'update_datetime',
                'worker_num',
                u_nick=F('user__nick')
            ).order_by('-id')
            data = {}
            data['code'] = 200
            data['history_list'] = list(history_list)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '未选择学校'})


# 4.回收人员登录
class LoginView(View):
    def post(self,request):
        log_num = request.POST.get('log_num')
        password = request.POST.get('password')
        print(log_num)
        print(password)
        if log_num and password:
            user_info = list(RecoveryPerson.objects.filter(log_num=log_num,password=password,is_use=0).values(
                'log_num',
                'school__id',
                'school__name')
            )
            print(user_info)
            if user_info:
                data = {}
                data['code'] = 200
                data['user_data'] = user_info
                return JsonResponse(data)
            else:
                return JsonResponse({'errmsg': '登录账号或者密码错误'})
        else:
            return JsonResponse({'errmsg': '未接收到数据'})
