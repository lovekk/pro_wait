from django.contrib import admin
from article.models import Article,ArticleComment



@admin.register(ArticleComment)
class Article_comment(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','comment_datetime','create_date','content','commentator','article']

    # 每页显示条数
    list_per_page = 10

@admin.register(Article)
class Article(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','short_content','editor','publish_date','view_num','author','school','is_show']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']







