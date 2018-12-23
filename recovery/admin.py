from django.contrib import admin
from recovery.models import MyRank,Price,Appoint,Bag,Introduction,Tips


# 回收预约
@admin.register(Appoint)
class AppointAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','thing_type','address','phone_num','remark','status','bag_num','money','user','school','create_date','create_time']

    # 每页显示条数
    list_per_page = 50

    # id 正序
    ordering = ['id']


# 回收排名
@admin.register(MyRank)
class MyRankAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','times','money','user','school','create_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 正序
    ordering = ['id']


# 回收价格
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','name','unit','price','create_datetime']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']


# 袋子信息
@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','number','create_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 正序
    ordering = ['id']



# 分类回收介绍
@admin.register(Introduction)
class IntroductionAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','content','create_datetime','update_datetime']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']


# 环保知识
@admin.register(Tips)
class TipsAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','school','tip','create_datetime','update_datetime']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']