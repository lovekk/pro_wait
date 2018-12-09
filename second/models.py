from django.db import models

# Create your models here.

# 二手市场
class Second(models.Model):
    type_choices = (
        (0, '全新'),
        (1, '九新'),
        (2, '半新'),
    )
    first_choices = (
        (0, '未置顶'),
        (1, '置顶'),
    )
    sale_choices = (
        (0, '未售出'),
        (1, '已出'),
    )

    content = models.CharField(max_length=300, default='', verbose_name='内容')
    price = models.IntegerField(verbose_name="价格",default=0)
    view_num = models.IntegerField(verbose_name="浏览量",default=0)
    good_num = models.IntegerField(verbose_name="点赞数",default=0)
    report_num = models.IntegerField(verbose_name="举报数",default=0)
    create_date = models.DateField(auto_now_add=True, verbose_name="日期")
    create_time = models.TimeField(auto_now_add=True, verbose_name="时间")
    is_first = models.SmallIntegerField(default=0, choices=first_choices, verbose_name='置顶')
    is_type = models.SmallIntegerField(default=1, choices=type_choices, verbose_name='新型')
    is_sale = models.SmallIntegerField(default=0, choices=sale_choices, verbose_name='出售')
    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey('user.User',verbose_name='发布者',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'dn_second'
        verbose_name = "校园二手发布"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


# 相关图片
class SecondImg(models.Model):
    qiniu_img = models.CharField(max_length=100, default='', verbose_name='七牛地址')
    local_img = models.ImageField(verbose_name='本地地址', upload_to='second/%Y/%m/%d', default='')
    second = models.ForeignKey('Second', verbose_name='校园二手', on_delete=models.CASCADE, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="日期时间")

    class Meta:
        db_table = 'dn_second_img'
        verbose_name = "校园二手图片"
        verbose_name_plural = verbose_name

