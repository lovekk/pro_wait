# pro_wait
《下课说》APP后台 
文件：setting.py和urls.py没有上传（在.gitignore中忽略了）  


## ---技术架构---
开发：Python3.6、Django2.0、MySQL5.7   
部署：Linux、Nginx、uWSGI、阿里云服务器
 

## ---简单总结---
### 一、数据表
共72张数据表，10张Django自带，62张自建表  
  <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/DYkauBs8CIh2hHS7PWGuuxP8RrMgC985oWIQwSf53L4!/b/dDYBAAAAAAAA&bo=CwSBAgAAAAADB64!&rf=viewer_4" width="800"/> 
  
### 二、django应用app
共10个django应用app 
1.activity 校园活动
2.article 九点读书  
3.culture 校园文化  
4.lose 失物招领  
5.moment 说说  
6.myhelp 校园帮助  
7.notice 校园公告  
8.recovery 垃圾分类回收  
9.second 校园二手  
10.user 用户  

  <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/GdVQcdu8zqua2cOD5Y5d9LiiuoRNwyCoH7ZOMgrUURI!/b/dLYAAAAAAAAA&bo=AgYYAwAAAAADJx0!&rf=viewer_4" width="800"/>   
  

### 三、后台（Django自带的admin管理后台）  
'
@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'content', 'tag', 'user', 'school','is_show', 'good_num', 'comment_num', 'view_num', 'relay_num',
                    'report_num', 'is_first', 'publish_date', 'publish_time']
    # 每页显示条数
    list_per_page = 50
    # id 排序
    ordering = ['-id']
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']
    # 筛选器
    list_filter = ['school', 'tag', 'report_num', 'is_show'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框
    date_hierarchy = 'publish_date'  # 详细时间分层筛选　日期时间用分层筛选
'

\*安卓和苹果显示效果不一样，苹果不允许显示关于金钱的字样    
部分示意图：   
  <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/3EEaUFgcOp0Hg5W79LTpMD*5yZ6oiu87Q7U6lIsYvE4!/b/dLYAAAAAAAAA&bo=OASABwAAAAADN6k!&rf=viewer_4" width="200"/> 
  <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/PmsbuislWiiZj4uB5VsCwxAteo4WHfKc*lU5bcImARE!/b/dL8AAAAAAAAA&bo=OASABwAAAAADJ7k!&rf=viewer_4" width="200"/>
  
    
### 四、消息  
1.新增粉丝  
2.评论留言查看  
3.私信聊天，即时通讯列表  
  
 部分示意图：   
  <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/s4n8hjnk9rUhESnNxr*5Vuer*MlyJudWwRzQkAa*b.A!/b/dL4AAAAAAAAA&bo=OASABwAAAAADJ7k!&rf=viewer_4" width="200"/> 
  <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/3CuaKWPeTW0kG78woo4hCNJrw.0IPOj2IFJEH*YPjbo!/b/dEkBAAAAAAAA&bo=OASABwAAAAADN6k!&rf=viewer_4" width="200"/>
  
    
### 五、我的  
1.展示本用户头像、用户名、学校、个性签名、粉丝数、关注数、积分  
2.查看我的主页，可删除发布的说说  
3.查看我的help，可删除发布的help  
4.个人信息修改，头像、用户名、学校、个性签名  
5.设置，修改密码、清楚缓存、查看已屏蔽用户  
6.查看关于我们，可文字留言  
7.在线客服联系  
8.退出账号进入登录注册页  
 
 部分示意图：   
  <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/*1lGHdY1fMCQx1VmZFxjm0L.s0A3VkJY.n*KAzQcVtA!/b/dD4BAAAAAAAA&bo=OASABwAAAAADJ7k!&rf=viewer_4" width="200"/> 
  <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/Iu07Hy2hf9P5bMgPtu3gsLWQla*ZGh3YUucqUqvK5As!/b/dDQBAAAAAAAA&bo=OASABwAAAAADF4k!&rf=viewer_4" width="200"/>
    <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/hR3wcgAdjy36S3vQ0z7kRLNu3yB*6I6buhoh.N4z9aQ!/b/dDIBAAAAAAAA&bo=OASABwAAAAADV8k!&rf=viewer_4" width="200"/>
    <img src="http://a4.qpic.cn/psb?/V14QvJYi1Zp3gm/0wX7YH441FlRgTM01TUxJkP4BeItbwwzl5MpGR9DEm0!/b/dL8AAAAAAAAA&ek=1&kp=1&pt=0&bo=OASABwAAAAADR9k!&tl=1&vuin=347699885&tm=1555304400&sce=60-2-2&rf=viewer_4" width="200"/>
  
#### *大半年的心血，真的不舍，百感交集~ 哎，有缘再见！
