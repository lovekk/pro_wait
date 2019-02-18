from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db.models import Count, F,Sum
from django.db import connection
from django.views.generic import View

from user.models import User, School, Follow, FunctionModule, AboutWe,AboutWeComment,RecoveryPerson, Login,Cj
from myhelp.models import Help
from activity.models import Activity
from article.models import Article
from moment.models import Moment, Video, Image, Voice, Tag, Good, Report

from utils.getModule import getModule
from utils.qiniu_upload import qi_local_upload, qi_upload
from pro_wait.settings import MEDIA_ROOT

import hashlib, copy,base64


# 测试首页
def index(request):
    return HttpResponse('ok')


# 测试json
def test_json(request):
    return JsonResponse({'name':'zk', 'num':123456})


# ========================================= 登录注册 ========================================
# 用户登录
def login(request):

    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')

        # 加密密码
        password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        obj = list(User.objects.filter(phone_num=phone_num).values('password'))
        if (obj):
            pwd = obj[0].get('password')
            print(pwd)
            print(password_md5)
            if str(pwd) == str(password_md5):
                user_msg = User.objects.filter(phone_num=phone_num).values('id','nick','head_image','head_qn_url','school','school__name','token')
                data = {}
                data['code'] = 200
                data['user_data'] = list(user_msg)
                print(data)
                return JsonResponse(data)
            else:
                return JsonResponse({'errmsg': '密码不正确!'})
        else:
            return JsonResponse({'errmsg': '此手机号未注册!'})
    else:
        return JsonResponse({'errmsg':'请求发生错误!'})


# 注册手机号是否已经使用
def register(request):
    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        is_have = User.objects.filter(phone_num=phone_num).exists()
        if is_have:
            return JsonResponse({'errmsg': '此手机号已经注册，可以直接登录!'})
        else:
            return JsonResponse({'code': 200})
    else:
        return JsonResponse({'errmsg':'请求发生错误!'})


# 注册 用户名 性别 学校 头像上传
def register_msg(request):
    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')

        nick = request.POST.get('nick')
        gender = request.POST.get('gender')
        school_id = request.POST.get('school_id')
        school_name = request.POST.get('school_name')

        device_num = request.POST.get('device_num')
        device_model = request.POST.get('device_model')
        device_name = request.POST.get('device_name')
        operator = request.POST.get('operator')
        reg_ip = request.POST.get('reg_ip')        # 注册IP
        system_type = request.POST.get('system_type')        # 手机系统类型
        channel = request.POST.get('channel')        # 下载渠道

        head_image = request.FILES.get('head_image')
        print(head_image)

        # 等号+1
        ac_num = list(User.objects.values('account_num').order_by('-id')[0:1])
        account_num = int(ac_num[0].get('account_num')) + 1
        print(account_num)

        # 测试为什么update不行 不能更新图片
        # head_image = request.FILES.get('head_image')
        # pic = User.objects.get(id=13)
        # pic.head_image = head_image
        # pic.save()

        # 先判断是否重名
        have_name = User.objects.filter(nick=nick).exists()
        if have_name:
            # 用户名已经存在
            return JsonResponse({'code': 400})

        # 先更新用户信息
        if phone_num and password and nick and head_image and school_id:
            # 加密
            password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
            # 创建
            user_create = User.objects.create(
                phone_num=phone_num,
                password=password_md5,
                nick=nick,
                gender=gender,
                school_id=school_id,
                account_num=account_num,
                school_name=school_name,
                device_num=device_num,
                device_model=device_model,
                device_name=device_name,
                operator=operator,
                head_image=head_image,
                reg_ip=reg_ip
            )
            data = {}
            if user_create:
                # 先保存到本地 不保存七牛 因为直接用七牛的put_data提示报错 期望不是InMemoryUploadedFile类型
                # 下面做七牛保存
                user_local_img = str(MEDIA_ROOT) + '/' + str(user_create.head_image)  # 拼接本地绝对路径
                qi_local_img = qi_local_upload(user_local_img)  # 七牛上传
                User.objects.filter(id=user_create.id).update(head_qn_url=qi_local_img)  # 更新七牛数据
                # 查询用户信息返回
                user_msg = User.objects.filter(id=user_create.id).values('id','nick','head_image','head_qn_url','school__id','school__name')

                # 返回用户信息
                data['code'] = 200
                data['user_msg'] = list(user_msg)

                print(data)
                return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '注册信息不全！'})
    else:
        return JsonResponse({'errmsg':'发生未知错误！'})


# 注册成功后 更新token
class UserToken(View):
    def post(self, request):
        user_id = request.POST.get('user_id')
        user_token = request.POST.get('user_token')
        if user_id and user_token:
            User.objects.filter(id=user_id).update(token=user_token)
            return JsonResponse({"code": 200})
        else:
            return JsonResponse({"errmsg":"没接收到"})


# ====================================学校 模块==================================================
# 学校列表
def school_list(request):
    if request.method == 'GET':
        school_list = School.objects.filter(is_show=True).values('id','name','province','city')
        data = {}
        data['code'] = 200
        data['list'] = list(school_list)
        return JsonResponse(data)
    else:
        return JsonResponse({'errmsg':'发生错误'})


# 根据学校id 选择不同的模块
# 校园活动 轮播图3张 id big_img
# 文章推荐 最新的前5篇
class FunctionModuleView(View):
    def get(self,request):
        school_id = request.GET.get('school_id')
        if school_id:
            modules = FunctionModule.objects.filter(school=school_id).values('module_name')
            # id倒序前3个 首页轮播图就3张
            activity = Activity.objects.filter(school=school_id, is_first=1).values('id', 'big_img').order_by('-id')[0:3]
            # id倒序前5个 显示5篇
            article = Article.objects.filter(is_show=1).values('id', 'title', 'view_num', 'list_img', 'author',
                                                                      'publish_date').order_by('-id')[0:5]
            data = {}
            data['code'] = 200
            data['modules'] = list(modules)
            data['activity'] = list(activity)
            data['article'] = list(article)
            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg':'未选择学校'})

# ================================================我的 关注 粉丝 积分 主页 修改个人信息================================
# 我自己的个人主页
class HomePage(View):
    def get(self,request):
        user_id = request.GET.get('user_id')
        if user_id:
            # 获赞数 评论数 粉丝数
            num_num = User.objects.filter(id=user_id).values('good_total','comment_total','fans_total')
            # 个人信息
            user = User.objects.filter(id=user_id).values('id', 'nick', 'head_qn_url','gender','school_name','my_sign')
            # 一对多 反查外键
            # 先查询 所有id
            moments_first = Moment.objects.filter(is_show=0,user=user_id).values('id').order_by('-id')

            data = {}
            for_one = {}  # 单次数据
            all_list = []  # 总数据

            # 遍历id
            for item in list(moments_first):
                # print(item.get('id'))  # {'id': 43}
                item_id = item.get('id')

                # 查发布内容
                for_t = Moment.objects.filter(id=item_id).values(
                    'id', 'content', 'good_num', 'publish_date', 'publish_time', 'tag', 'comment_num', 'view_num',
                    'comment_num',u_nick=F('user__nick'), u_img=F('user__head_qn_url'), u_id=F('user__id'))

                for_text = list(for_t)
                # 查发布图片
                for_img = list(Image.objects.filter(moment=item_id).values('id', 'qiniu_img', 'moment'))
                # 查看 录音
                for_voice = list(
                    Voice.objects.filter(moment=item_id).values('id', 'qiniu_voice', 'local_voice', 'voice_time','moment'))
                # 查看 视频
                for_video = list(Video.objects.filter(moment=item_id).values('id', 'qiniu_video', 'moment'))
                # 是否点赞
                for_good = Good.objects.filter(moment=item_id, user=user_id).exists()

                for_one['id'] = item_id
                for_one['for_text'] = for_text
                for_one['for_img'] = for_img
                for_one['for_voice'] = for_voice
                for_one['for_video'] = for_video
                for_one['for_good'] = for_good
                # 单个 追加
                all_list.append(copy.deepcopy(for_one))
                # print(for_one)

            data['code'] = 200
            data['num_num'] = list(num_num)
            data['user_list'] = list(user)
            data['all_list'] = all_list
            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg": "用户不存在"})


# ta的个人主页
class HisHomePage(View):
    def get(self,request):
        user_id = request.GET.get('user_id')
        my_id = request.GET.get('my_id')
        skip = int(request.GET.get('skip'))  # 分页
        if user_id:
            end_skip = skip + 10
            # # 获赞数 评论数
            # moment_num = Moment.objects.filter(user=user_id).aggregate(Sum('good_num'),Sum('comment_num'))
            # # 粉丝数
            # fans_num = Follow.objects.filter(follow_id=user_id,is_delete=0).aggregate(Count('user'))

            # 获赞数 评论数 粉丝数
            num_num = User.objects.filter(id=user_id).values('good_total','comment_total','fans_total')
            # 个人信息
            user = User.objects.filter(id=user_id).values('id', 'nick', 'head_qn_url','gender','school_name','my_sign')
            # 一对多 反查外键
            # 先查询 所有id----匿名的不显示
            moments_first = Moment.objects.filter(is_show=0, user=user_id).exclude(tag='匿名树洞').values('id').order_by('-id')[skip:end_skip]

            data = {}
            for_one = {}  # 单次数据
            all_list = []  # 总数据

            # 遍历id
            for item in list(moments_first):
                # print(item.get('id'))  # {'id': 43}
                item_id = item.get('id')

                # 查发布内容
                for_t = Moment.objects.filter(id=item_id).values(
                    'id', 'content', 'good_num', 'publish_date', 'publish_time', 'tag', 'comment_num', 'view_num',
                    'comment_num',u_nick=F('user__nick'), u_img=F('user__head_qn_url'), u_id=F('user__id'))

                for_text = list(for_t)
                # 查发布图片
                for_img = list(Image.objects.filter(moment=item_id).values('id', 'qiniu_img', 'moment'))
                # 查看 录音
                for_voice = list(
                    Voice.objects.filter(moment=item_id).values('id', 'qiniu_voice', 'local_voice', 'voice_time','moment'))
                # 查看 视频
                for_video = list(Video.objects.filter(moment=item_id).values('id', 'qiniu_video', 'moment'))
                # 是否点赞
                for_good = Good.objects.filter(moment=item_id, user=user_id).exists()

                for_one['id'] = item_id
                for_one['for_text'] = for_text
                for_one['for_img'] = for_img
                for_one['for_voice'] = for_voice
                for_one['for_video'] = for_video
                for_one['for_good'] = for_good
                # 单个 追加
                all_list.append(copy.deepcopy(for_one))
                # print(for_one)

            # 查看是否关注
            if user_id == my_id:
                data['follow'] = 2
            else:
                is_follow = Follow.objects.filter(follow_id=user_id, user=my_id, is_delete=0).exists()
                if is_follow:
                    # 已经关注了
                    data['follow'] = 1
                else:
                    data['follow'] = 0  #没有关注

            data['code'] = 200
            data['num_num'] = list(num_num)
            data['user_list'] = list(user)
            data['all_list'] = all_list
            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg": "改用户不存在"})


#我的关注
class MyFollow(View):
    def get(self,request):
        user_id = request.GET.get('user_id')
        if user_id:
            # 查询出所有的关注
            data = {}
            # 不用深拷贝 遍历追加的方法
            # follows = Follow.objects.filter(user=user_id, is_delete=0).values('follow_id').order_by('-id')
            # for follow_item in list(follows):
            #     print(follow_item)
            #     # 获取id
            #     for_u_id = follow_item.get('follow_id')
            #     follow_one = User.objects.filter(id=for_u_id).values('nick','head_qn_url','school_name')
            #     # 字典
            #     follow_item['follow_one'] = list(follow_one)

            follow_u_id = []
            # 找到所有follow_id
            follows = list(Follow.objects.filter(user=user_id,is_delete=0).values('follow_id').order_by('-id'))
            # 追加到一个列表里面
            for item in follows:
                print(item)
                one_id = item['follow_id']
                follow_u_id.append(one_id)
            # 用户id 在这个列表里
            follow_list = User.objects.filter(id__in=follow_u_id).values('id', 'nick','head_qn_url','school_name')

            data['code'] = 200
            data['follow_list'] = list(follow_list)

            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg": "用户不存在"})


# 我的粉丝
class MyFans(View):
    def get(self,request):
        user_id = request.GET.get('user_id')
        if user_id:
            fans = Follow.objects.filter(follow_id=user_id,is_delete=0).values(
                u_id = F('user__id'),
                u_nick = F('user__nick'),
                u_head_img = F('user__head_qn_url'),
                u_school_name = F('user__school_name')
            ).order_by('-id')
            data = {}
            data['code'] = 200
            data['fans'] = list(fans)
            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg": "用户不存在"})


# 我的积分 关注数 积分数
class MyNum(View):
    # 总积分，help积分，垃圾回收积分
    def get(self,request):
        user_id = request.GET.get('user_id')
        if user_id:
            # # 积分数
            # integral_total = User.objects.get(id=user_id).integral
            # # 粉丝数
            # fans_num = Follow.objects.filter(follow_id=user_id,is_delete=0).aggregate(Count('user'))
            # # 关注数量数
            # follow_num = Follow.objects.filter(user=user_id,is_delete=0).aggregate(Count('follow_id'))

            my_num = User.objects.filter(id=user_id).values('head_qn_url','nick','school_name','integral','fans_total','create_total')
            data = {}
            data['code'] = 200
            data['my_num'] = list(my_num)
            return JsonResponse(data)
        else:
            return JsonResponse({"errmsg": "改用户不存在"})


# 更新个人信息
class UpdateUserInfoView(View):
    def post(self,request):
        user_id = request.POST.get('user_id')
        if user_id:
            nick = request.POST.get('nick')
            password = request.POST.get('password')
            head_image = request.FILES.get('head_image')
            my_sign = request.POST.get('my_sign')

            User.objects.filter(id=user_id).update(nick=nick,password=password,head_image=head_image,my_sign=my_sign)

        else:
            return JsonResponse({'errmsg':'该用户不存在'})


# 更新个人信息 头像
class UpdateUserHeadView(View):
    def post(self,request):
        user_id = request.POST.get('user_id')
        if user_id:
            nick = request.POST.get('nick')
            password = request.POST.get('password')
            head_image = request.FILES.get('head_image')
            my_sign = request.POST.get('my_sign')

            User.objects.filter(id=user_id).update(nick=nick,password=password,head_image=head_image,my_sign=my_sign)

        else:
            return JsonResponse({'errmsg':'该用户不存在'})


# ================================================关于我们================================
# 关于我们
class AboutWeView(View):
   def get(self,request):
        skip = int(request.GET.get('skip'))  # 分页
        end_skip = skip + 20

        about_we = AboutWe.objects.values()
        comment = AboutWeComment.objects.values(
            'comment',
            'create_date',
            nick = F('user__nick'),
            u_img=F('user__head_qn_url'),
            u_id=F('user__id')
        ).order_by('-id')[skip:end_skip]

        if about_we :
            data = {}
            data['code'] = 200
            data['about_we_data'] = list(about_we)
            data['comment_data'] = list(comment)

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg':'请求发生错误'})


# 关于我们 添加评论
class AddAboutCommentView(View):
    def post(self,request):
        comment = request.POST.get('comment')
        commentator_id = request.POST.get('commentator_id')

        if commentator_id:
            user = User.objects.get(id=commentator_id)
            comment_creat = AboutWeComment.objects.create(comment=comment,user=user)
            if comment_creat:
                return JsonResponse({'code':200})
            else:
                return JsonResponse({'errmsg': '评论失败'})
        else:
            return JsonResponse({'errmsg': '没有接收到数据'})


#登录 保存登录信息
class LoginView(View):
    def post(self,request):
        phone_num = request.POST.get('phone_num')  #电话号码
        password = request.POST.get('password')    #密码
        log_ip = request.POST.get('log_ip')        #登录IP
        device_num = request.POST.get('device_num') #设备唯一标识
        device_model = request.POST.get('device_model') #设备型号
        device_name = request.POST.get('device_name')   #设备名称
        operator = request.POST.get('operator')         #设备运营商名称
        system_type = request.POST.get('system_type')         #手机系统类型
        system_version = request.POST.get('system_version')         #手机平台系统版本
        connection_type = request.POST.get('connection_type')         #网络连接类型
        screen_width = request.POST.get('screen_width')         #屏幕分辨率宽
        screen_height = request.POST.get('screen_height')         #屏幕分辨率高
        channel = request.POST.get('channel')         #渠道
        jail_break = request.POST.get('jail_break')         #设备是否越狱

        # 只做简单的保存
        user = User.objects.get(phone_num=phone_num)

        save_login = Login.objects.create(phone_num=phone_num, password=password, log_ip=log_ip,device_model=device_model,
                                          device_num=device_num, device_name=device_name,operator=operator,
                                          system_type=system_type,system_version=system_version,connection_type=connection_type,
                                          screen_width=screen_width,screen_height=screen_height,jail_break=jail_break,user=user)
        if save_login :
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg':'未接收到数据！'})

# 忘记密码
class ForgetPwd(View):
    def post(self,request):
        # user_id = request.POST.get('user_id')
        phone_num = request.POST.get('phone_num')  # 手机号
        password = request.POST.get('password')  # 新密码
        re_password = request.POST.get('password') # 确认新密码

        if phone_num and password and re_password:
            is_have = User.objects.filter(phone_num=phone_num).exists()
            if is_have:
                if password == re_password:
                    User.objects.filter(phone_num=phone_num).update(password=password)
                else:
                    return JsonResponse({'errmsg':'两次密码输入不一致！'})
            else:
                return JsonResponse({'errmsg':'手机号未注册！'})
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg':'未接收到数据！'})


# 修改密码
class ChangePwd(View):
    def post(self,request):
        user_id = request.POST.get('user_id')
        init_pwd = request.POST.get('old_pwd')  #初始密码
        new_pwd = request.POST.get('new_pwd')  # 新密码
        confirm_pwd = request.POST.get('confirm_pwd') # 确认新密码

        # 加密
        init_pwd_md5 = hashlib.md5(init_pwd.encode(encoding='UTF-8')).hexdigest()
        new_pwd_md5 = hashlib.md5(new_pwd.encode(encoding='UTF-8')).hexdigest()

        # 判断密码情况
        if user_id and init_pwd and new_pwd and confirm_pwd:
            # 获取到当前对象
            user_pwd = User.objects.get(id=user_id)
            if init_pwd_md5 == user_pwd.password:
                if new_pwd == confirm_pwd:
                    # 更新密码
                    User.objects.filter(id=user_id).update(password=new_pwd_md5)
                    return JsonResponse({'code': 200})
                else:
                    return JsonResponse({'errmsg': '两次密码输入不一致'})
            else:
                # 初始密码不正确
                return JsonResponse({'code': 400})
        else:
            return JsonResponse({'errmsg':'未接收到参数'})


#  保存成绩、学生认证、查询成绩 2019/1/23
class SchoolAuth(View):
    def post(self, request):
        school_id = request.POST.get('school_id')
        user_id = request.POST.get('user_id')
        account = request.POST.get('account')  # 学号
        password = request.POST.get('password')
        code = request.POST.get('code')  # 验证码

        data = {}

        if account and password and code:
            # 获取不同学校里的方法
            module = getModule(school_id)
            real_name = module.login(account, password, code)

            # 这不是第一次
            if User.objects.filter(id=user_id, real_name=real_name).exists():
                # 调用保存成绩的方法
                module.getCj(user_id, school_id)
                # 查询成绩
                cj = Cj.objects.filter(user=user_id, school=school_id).values()
                if cj:
                    data['code'] = 200
                    data['cj'] = list(cj)
                    return JsonResponse(data)
                else:
                    return JsonResponse({"errmsg": "没查询到成绩"})

            # 第一次 更新用户信息
            else:
                # 保存真实姓名到数据库，完成实名验证
                User.objects.filter(id=user_id).update(real_name=real_name, stu_num=account, stu_password=password,
                                                       is_school_auth=1)
                # 调用保存成绩的方法
                module.getCj(user_id, school_id)
                # 查询成绩
                cj = Cj.objects.filter(user=user_id).values()
                if cj:
                    data['code'] = 200
                    data['cj'] = list(cj)
                    return JsonResponse(data)
                else:
                    return JsonResponse({"errmsg": "没查询到成绩"})

        # 如果教务系统没有验证码
        elif code is None and account and password:
            module = getModule(school_id)
            real_name = module.login(account, password)
            if User.objects.filter(id=user_id, real_name=real_name).exists():
                # 调用保存成绩的方法
                module.getCj(user_id, school_id)
                # 查询成绩
                cj = Cj.objects.filter(user=user_id, school=school_id).values()
                if cj:
                    data['code'] = 200
                    data['cj'] = list(cj)
                    return JsonResponse(data)
                else:
                    return JsonResponse({"errmsg": "没查询到成绩"})
            else:
                # 保存真实姓名到数据库，完成实名验证
                User.objects.filter(id=user_id).update(real_name=real_name, stu_num=account, stu_password=password,
                                                       is_school_auth=1)
                # 调用保存成绩的方法
                module.getCj(user_id, school_id)
                # 查询成绩
                cj = Cj.objects.filter(user=user_id, school=school_id).values()
                if cj:
                    data['code'] = 200
                    data['cj'] = list(cj)
                    return JsonResponse(data)
                else:
                    return JsonResponse({"errmsg": "没查询到成绩"})

        else:
            return JsonResponse({"errmsg": "没接收到学号或者密码"})


# 返回验证码图片
def getCodeImage(request):
    if request.method == 'GET':
        school_id = request.GET.get('school_id')
        module = getModule(school_id)
        code_img = module.getcode()
        print(code_img)
        return JsonResponse({"code_img": str(code_img)})