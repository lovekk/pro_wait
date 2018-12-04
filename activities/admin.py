from django.contrib import admin
from activities.models import Activites,Activites_comment

@admin.register(Activites_comment)
class Activites_comment(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','comment_date','content','commentator','activites']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']

@admin.register(Activites)
class Activites(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','introduction','content','editor','publish_date','view_num','school']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']





# admin.site.register(User, UserAdmin)
# admin.site.register(School, SchoolAdmin)



