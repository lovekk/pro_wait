from django.contrib import admin
from article.models import Article,ArticleComment


# 九点读书 文章
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','short_content','author','editor','is_all_school','is_original','publish_date','view_num','school','is_show']

    # 每页显示条数
    list_per_page = 20

    # id 正序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'title']

    # 筛选器
    list_filter = ['school', 'is_all_school', 'is_original', 'is_show'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['title']  # 搜索字段 标题等文本字段用搜索框


# 九点读书 文章评论
@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','comment_datetime','create_date','content','commentator','article']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框


