from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from .models import Price, Appoint, MyRank, Bag, Introduction, Tips
from user.models import User, School
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

                # 我的排名表里面的积分要更新，投递次数更新
                is_my_rank = MyRank.objects.filter(id=user_id).exists()
                if is_my_rank:
                    # 如果存在

                    # 更新回收排行次数
                    user = User.objects.get(id=user_id)
                    my_rank_id = user.myrank.id
                    my_rank = MyRank.objects.get(id=my_rank_id)
                    times = my_rank.times + 1
                    # 更新回收排行积分
                    appoint = Appoint.objects.get(id=appoint_id)
                    money = my_rank.money + appoint.money
                    MyRank.objects.filter(id=my_rank_id).update(times=times,money=money)

                    # 更新该用户总积分
                    integral = user.integral + money
                    User.objects.filter(id=user_id).update(integral=integral)
                else:
                    # 不存在 就创建
                    # 外键实例
                    school_ins = School.objects.get(id=school_id)
                    user_ins = User.objects.get(id=user_id)
                    my_rank_create = MyRank.objects.create(times=1, money=0, user=user_ins, school=school_ins)


                return JsonResponse({"code": 200})
            else:
                return JsonResponse({"errmsg": "您还没有预约！"})
        else:
            return JsonResponse({"errmsg":"您绑定的回收袋不存在！"})


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
