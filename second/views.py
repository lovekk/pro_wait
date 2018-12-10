
from django.http import JsonResponse
from django.views.decorators.http import require_POST,require_GET
from django.views.generic import View
from django.db.models import Count, F

from utils.qiniu_upload import qi_local_upload
from pro_wait.settings import MEDIA_ROOT

from second.models import Second, SecondImg
from user.models import User, School

import copy

# Create your views here.


# 校园二手 列表
@require_GET
def second_list(request):
    pass


# 添加 发布 校园二手
@require_POST
def second_add(request):
    pass


# 类视图方式写
# 校园二手 列表
class IndexView(View):
    def get(self, request):
        school_id = request.GET.get('school_id')
        if school_id:
            # 一对多 反查外键
            # 先查询 所有id
            seconds_list = Second.objects.filter(school=school_id, is_first=0).values('id', 'content','price',
                'good_num', 'create_date', 'create_time', 'is_type', u_nick=F('creator__nick'),
                u_img=F('creator__head_image'), u_id=F('creator__id'), u_token=F('creator__token')).order_by('-id')

            data = {}
            for_all = {}  # 单次数据
            all_list = []  # 总数据

            # 遍历id
            for item in list(seconds_list):
                # print(item.get('id'))  # {'id': 43}
                item_id = item.get('id')
                # 查发布图片
                for_all['for_img'] = list(SecondImg.objects.filter(second=item_id).values('id', 'qiniu_img', 'second'))
                all_list.append(copy.deepcopy(for_all))
                # print(for_all)

            data['code'] = 200
            data['text_list'] = list(seconds_list)
            data['img_list'] = all_list

            return JsonResponse(data)
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})


# 添加 发布 校园二手
class AddView(View):
    def post(self, request):
        # 获取ajax数据
        school_id = request.POST.get('school_id')
        creator_id = request.POST.get('creator_id')
        # content = request.POST.get('content').replace("\n","</br>")  # 没法换行
        content = request.POST.get('content')
        price = int(request.POST.get('price'))
        is_type = int(request.POST.get('is_type'))

        # 获取ajax图片
        img_list = request.FILES.getlist('img_list')

        if school_id and creator_id:
            # 保存文本数据
            user_ins = User.objects.get(id=creator_id)
            school_ins = School.objects.get(id=school_id)
            second_create = Second.objects.create(content=content, is_type=is_type, price=price,
                                              school=school_ins, creator=user_ins)

            # 保存 外键的 图片数据
            # 这一块 写的 绝望  这次再看看 还好 总感觉不是最优写法
            if img_list and second_create:
                for img in img_list:
                    # 先保存到本地 不保存七牛 因为直接用七牛的put_data提示报错 期望不是InMemoryUploadedFile类型
                    # 不怕图片名称重复 django处理了
                    save_img = SecondImg.objects.create(local_img=img, second=second_create)

                    # 下面做七牛保存
                    second_local_img = str(MEDIA_ROOT) + '/' + str(save_img.local_img)  # 拼接本地绝对路径
                    second_img_id = save_img.id  # 获取当前本地图片的id
                    qi_local_img = qi_local_upload(second_local_img)  # 七牛上传
                    SecondImg.objects.filter(id=second_img_id).update(qiniu_img=qi_local_img)  # 更新七牛数据

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'errmsg': '尚未选择学校'})




