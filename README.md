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
```
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
```
   
  <img src="http://m.qpic.cn/psb?/V14QvJYi1Zp3gm/glEHsk2.2DIlo5cDlO.0ehdDrB5l7SmHJ46xMJLdiCU!/b/dL8AAAAAAAAA&bo=jgS9AwAAAAADBxY!&rf=viewer_4" width="800"/> 
  
  
    
### 四、其他  
1.音视图，先保存到本地服务器，再上传到七牛云，手机APP端直接使用七牛存储地址  
2.utils封装模块，七牛存储，课表成绩的爬取  
  
  
未完待续，有时间再详细补充......

  
 
