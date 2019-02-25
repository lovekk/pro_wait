from django.contrib import admin
from recovery.models import MyRank,Price,Appoint,Bag,Introduction,Tips


# 回收预约
@admin.register(Appoint)
class AppointAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','thing_type','address','phone_num','remark','status','bag_num','money','weight','user','school',
                    'worker_num','create_date','create_time','update_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 正序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'thing_type']

    # 筛选器
    list_filter = ['status', 'school', 'worker_num'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['thing_type']  # 搜索字段 标题等文本字段用搜索框


# 回收排名
@admin.register(MyRank)
class MyRankAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','times','money','user','school','create_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 正序
    ordering = ['money']


# 回收价格
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','name','unit','price','create_datetime']

    # 每页显示条数
    list_per_page = 50

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
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'number']

    # 筛选器
    search_fields = ['number']  # 搜索字段 标题等文本字段用搜索框



# 环保知识分类回收介绍
@admin.register(Introduction)
class IntroductionAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','content','create_datetime','update_datetime']

    # 每页显示条数
    list_per_page = 20

    # id 正序
    ordering = ['id']


# 每个学校的提示
@admin.register(Tips)
class TipsAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','school','tip','create_datetime','update_datetime']

    # 每页显示条数
    list_per_page = 20

    # id 正序
    ordering = ['id']