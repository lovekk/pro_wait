from django.db import models
from tinymce.models import HTMLField

# 分类回收 预约表
class Appoint(models.Model):
    thing_type = models.CharField(max_length=100,verbose_name="物品类别", default="")
    address = models.CharField(max_length=100,verbose_name="预约地址", default="")
    phone_num = models.CharField(max_length=50, verbose_name="手机号", default="")
    remark = models.CharField(max_length=200,verbose_name="备注",default="")
    money = models.IntegerField(verbose_name="单次回收积分整数",default=0)
    weight = models.DecimalField(max_digits=6,decimal_places=2,verbose_name="重量小数",default=0.0)
    bag_num = models.CharField(max_length=30,verbose_name="袋子编号", default="")
    worker_num = models.CharField(max_length=30,verbose_name="称重工作人员编号", default="")
    create_date = models.DateField(auto_now_add=True, verbose_name="预约创建日期")
    create_time = models.TimeField(auto_now_add=True, verbose_name="预约创建时间")
    update_datetime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    status = models.SmallIntegerField(default=0, choices=((0, '已预约'), (1, '已绑袋'), (2, '回收完成 ')), verbose_name='回收状态')

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_recovery_appoint'
        verbose_name = "回收·预约"
        verbose_name_plural = verbose_name


# 分类回收 我的回收记录排名
class MyRank(models.Model):
    times = models.IntegerField(verbose_name="回收次数", default=0)
    money = models.IntegerField(verbose_name="回收总积分", default=0)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    user = models.OneToOneField('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_recovery_rank'
        verbose_name = "回收·排名榜"
        verbose_name_plural = verbose_name


# 分类回收 回收物品价格信息表
class Price(models.Model):
    name = models.CharField(max_length=50,verbose_name="物品名称", default="")
    unit = models.CharField(max_length=20,verbose_name="物品单位", default="")
    price = models.DecimalField(max_digits=6,decimal_places=2,verbose_name="物品价格", default=1.00)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'dn_recovery_price'
        verbose_name = "回收·物品价格"
        verbose_name_plural = verbose_name


# 分类回收 袋子表
class Bag(models.Model):
    number = models.CharField(max_length=30,verbose_name="袋子编号", default="")
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = 'dn_recovery_bag'
        verbose_name = "回收·袋子编号"
        verbose_name_plural = verbose_name


# 分类回收 预约提示信息
class Tips(models.Model):
    tip = models.TextField(verbose_name="预约学校宿舍提示信息", default="")
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_datetime = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_recovery_tips'
        verbose_name = "回收·学校提示"
        verbose_name_plural = verbose_name


# 分类回收 环保知识简介
class Introduction(models.Model):
    content = HTMLField(verbose_name="环保知识介绍")
    view_num = models.IntegerField(verbose_name="全国浏览量", default=0)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_datetime = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'dn_recovery_introduction'
        verbose_name = "回收·环保知识介绍"
        verbose_name_plural = verbose_name




