from django.contrib import admin
from article.models import Article,Article_comment



@admin.register(Article_comment)
class Article_comment(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','comment_date','content','commentator','article']

    # 每页显示条数
    list_per_page = 10

@admin.register(Article)
class Article(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','content','editor','publish_date','view_num','author','school']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']







