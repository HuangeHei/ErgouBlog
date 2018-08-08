from django.shortcuts import render,HttpResponse
from blog.Auth import Auth
from blog import dataHelper as db
from blog.helper.upLoad import Upload
from blog.helper.test_do import Test
from ErgouBlog.settings import FILE_TEMP
import json

import logging

log = logging.getLogger('log')

# Create your views here.

#----------------------------------------- 用户登录相关 开始 -------------------------------------------------

''' 用户登录

    /login/  post 方式

    参数 {
            user_name:'123',
            user_passwd:'123'
        }

        登录成功
        {
            "status": true          # 返回登录状态
            "user_name":"huanghei"  # 返回登录的用户名
            "user_id":"123"         # 返回用户id
        }
        登录失败
        {
            "status":false
            "error":'用户名或密码错误!'
        }
        如果账号或密码为空
        {   
            'status':false,
            'error':'用户名密码为空!'
        }
'''


def login(request):
    if request.method == 'POST':

        user_name = request.POST.get('user_name', False)
        user_passwd = request.POST.get('user_passwd', False)

        if user_name and user_passwd:

            ret_login = Auth.is_login(user_name, user_passwd, request)


            if ret_login['status']:

                log.info("用户登录成功 USER_NAME:%s" % user_name)

                return HttpResponse(json.dumps({
                    'status': True,
                    'user_id':request.session['user_id'],
                    'user_name':request.session['user_name']
                }))

            else:

                log.error(ret_login['error'])

                return HttpResponse(json.dumps({
                    'status': False,
                    'error': ret_login['error']
                }))

        else:

            log.error("用户名密码为空")

            return HttpResponse(json.dumps({
                'status': False,
                'error': '用户名密码为空!'
            }))

    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')


''' 用户注销

    /out/  post 方式

        注销成功
        {
            "status": true
        }
        注销失败
        {
            "status":false
            "error":'error'
        }
'''


def out(request):
    if request.method == 'POST':

        ret = Auth.out_login(request)

        if ret['status']:

            log.info("用户注销成功")

            return HttpResponse(json.dumps({
                'status': True
            }))

        else:

            log.error("用户注销失败 错误信息:%s" % ret['error'])

            return HttpResponse(json.dumps({
                'sataus': False,
                'error': ret['error']
            }))

    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')


'''获取用户登录属性

    /get_login/  get 方式

        获取成功
        {
            "status": true
            "user_name": 'user_name'
            "user_id":'123'
        }
        获取失败
        {
            "status":false
        }

'''


def get_login_status(request):

    if request.method == 'GET':

        ret = Auth.login_status(request)

        if ret['status']:

            log.info("获取用户登录状态成功")

            return HttpResponse(json.dumps(ret))

        else:

            log.info("获取用户登录状态失败")

            return HttpResponse(json.dumps({
                'status': False
            }))

    else:

        log.error("错误的访问，无 POST")

        return HttpResponse('not post')



'''搜索文章标题或文章内容

    /search/  post 方式

    参数：{
             search:搜索的内容
         }


        搜索到内容
        [
            {
                "article_text": "进哥是大傻逼",
                "article_ding": 1,
                "article_title": "我是python文章标题",
                "article_modify_date": "2018-06-07 14:03:21",
                "user_name": "Huanghei",
                "article_id": 4,
                "article_class": "Django 分类",
                "article_is_save": false,
                "user_id": 2,
                "article_pageviews": 1,
                "article_date": "2018-06-07 14:03:21",
                "article_class_id": 4
            }
        ]
        搜索不到内容
        {
            "status": false,
            "error": "搜索不到您要的内容哦~",       
        }
'''


def serach(request):

    if request.method == 'POST':

        search = request.POST.get('serach', False)

        if search:
            return HttpResponse(json.dumps(db.search(search)))
            log.info('获取成功')
        else:

            log.info("搜索内容为空")

            return HttpResponse(json.dumps({
                'status': False,
                'error': '搜索内容为空'
            }))

    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')



#------------------------------------------ 用户登录相关 结束 ------------------------------------------------


#----------------------------------------- 前端展示,无需权限 开始 ---------------------------------------------

"""
    返回主页设置
    
    /get_index_setting/  get 方式
    
    返回值
        {
            "index_setting": "随便写",
            "index_head_color": "#545454",
            "index_notice": "我是来逗比的公告~"
        }
"""


def get_index_setting(request):

    if request.method == 'GET':

        log.info("获取主页设置")

        return HttpResponse(db.site_info())

    else:

        log.error("错误的访问，无 POST")

        return HttpResponse('not post')




"""
    返回所有用户

    /get_user_list/  get 方式

    返回值
        [
            {
                "user_id": 1,
                "user_name": "huanghei"
            }
        ]
"""

def get_user_list(request):

    '''request.method.lower() 可以获取到request请求方式'''

    if request.method == 'GET':

        log.info('获取了全部用户列表')

        return HttpResponse(db.get_user_list())

    else:

        log.error("错误的访问，无 POST")

        return HttpResponse('not post')


"""
    返回所有分类

    /get_article_class/  post 方式
    
    可传参数 user_id  不传参数  返回所有用户分类

    返回值
        [
            {
                "user_id": 1,
                "class_id": 1,
                "class_name": "HTML 分类",
                "user_name": "Kong"
            },
            {
                "user_id": 1,
                "class_id": 2,
                "class_name": "CSS 分类",
                "user_name": "Kong"
            },
            {
                "user_id": 1,
                "class_id": 13,
                "class_name": "SB 分类",
                "user_name": "Kong"
            }
        ]
    
"""


def get_article_class(request):

    if request.method == 'POST':

        if request.POST.get('user_id',False):

            user_id = request.POST['user_id']

            log.info('获取用户文章分类USER_ID:%s' % user_id)

            return HttpResponse(db.get_article_class(user_id = user_id))

        else:

            log.info('获取所有用户文章分类')

            return HttpResponse(db.get_article_class())
    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')



'''
    /get_article/  post 方式
    参数 article_id 或者 user_id 或者 什么都不传
    传递 user_id    返回 用户的所有文章
    传递 article_id 返回 单篇文章
    什么都不传       返回 所有文章
    
    返回值
    [
        {
            "article_modify_date": "2018-06-07 14:02:10",
            "article_id": 1,
            "article_title": "我是HTML文章标题",
            "article_is_save": false,
            "article_pageviews": 1,
            "user_name": "Kong",
            "user_id": 1,
            "article_class": "HTML 分类",
            "article_date": "2018-06-07 14:02:10",
            "article_text": "我是HTML文章内容",
            "article_ding": 1
        },
        {
            "article_modify_date": "2018-06-07 14:02:48",
            "article_id": 2,
            "article_title": "我是CSS文章标题",
            "article_is_save": false,
            "article_pageviews": 1,
            "user_name": "Kong",
            "user_id": 1,
            "article_class": "CSS 分类",
            "article_date": "2018-06-07 14:02:48",
            "article_text": "我是CSS文章内容",
            "article_ding": 1
        },
    ]

 
'''

def get_article(request):

    if request.method == 'POST':

        if request.POST.get('user_id',False):

            user_id = request.POST['user_id']

            log.info('获取用户所有文章 USER_ID:%s' % user_id)

            return HttpResponse(db.get_article(user_id = user_id))

        elif request.POST.get('article_id',False):


            try:

                article_id = request.POST.get('article_id',False)

                log.info('获取文章 ARTICLE_ID:%s' % article_id)

                return HttpResponse(db.get_article(article_id))

            except Exception as E:

                log.error("获取单个文章出错 错误信息:%s" % E)

                return HttpResponse(json.dumps({
                    'status':False,
                    'error':'获取单个文章出错，详细见日志'
                }))

        else:

            try:

                log.info('获取文章获取全部文章')

                return HttpResponse(db.get_article())

            except Exception as E:

                log.error("获取全部文章错误 错误信息:%s" % E)

                return HttpResponse(json.dumps({
                    'status':False,
                    'error':'获取全部文章错误，错误信息:%s' % E
                }))




    else:

        log.error("错误的访问，无 GET")

        return HttpResponse("not get")



'''
    /get_user_site_setting/  post 方式
    
    参数 user_id

    返回值用户设置
        {
            "blog_name": "Kong",
            "blog_bgm": null,
            "blog_head_color": "#545454",
            "blog_info": "怕是个肥狗子哦！"
        }
'''


def get_user_site_setting(request):

    if request.method == 'POST':

        if request.POST.get('user_id',False):

            user_id = request.POST['user_id']

            log.info('获取用户设置 USER_ID:%s' % user_id)

            return HttpResponse(db.get_user_setting(user_id))

        else:

            log.error('获取用户设置失败，因为没有USER_ID')

            return HttpResponse(json.dumps({
                'status':False,
                'error':'请给我一个用户ID!'
            }))


    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')

def reg_user(request):

    if request.method == 'POST':

        if request.POST.get('user_name', False) and request.POST.get('user_passwd', False):

            ret = db.create({
                'user_name':request.POST.get('user_name', False),
                'user_passwd':request.POST.get('user_passwd', False)
            })

            return HttpResponse(ret)

        else:

            log.error('创建用户失败，检查post数据')

            return HttpResponse(json.dumps({
                'status': False,
                'error': '创建用户失败，检查post数据'
            }))


    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')

#----------------------------------------- 前端展示,无需权限 结束 ---------------------------------------------

#----------------------------------------- 前端后台设置,需要权限 开始 ---------------------------------------------

'''
    /upload/  post 方式
    
    参数 ajax方式的话  {
        'file':file
    }要保存的文件,插件上传图片，或者表单上传图片则不需要key
    

    返回值 上传成功 和 文件名称
        {
            'status':True,
            'name': 'xxxxxxxxxxxxx'
        }
        
        上传失败
        {
            'status':False,
            'error':'写入失败'
        }
'''

@Auth.auth()
def upload_file(request):

    if request.method == 'POST':

        up_obj = Upload(request.FILES['file'],FILE_TEMP) # 创建up_obj 对象

        try:

            file = up_obj.upfile_save()

        except Exception as E:

            log.error('写入失败 原因:%s' % E)

            return HttpResponse(json.dumps({
                'status':False,
                'error':'写入失败 原因:%s' % E
            }))

        log.error('文件上传成功 %s' % request.session['user_name'])

        return HttpResponse(json.dumps({
            'status':True,
            'name': file
        }))

    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')


''' 设置index 页面信息

    /set_index/  post   方式

    参数  
        {
            index_setting
            index_head_color
            index_notice
        }

    返回值 成功
        {
            'status':True,
        }

        失败

        {
            'status':False,
            'error':'xxxx'
        }
'''


@Auth.auth()
def set_index(request):

    if request.method == 'POST':
        try:
            data = {
                'index_setting':request.POST.get('index_setting', None),
                'index_head_color':request.POST.get('index_head_color', None),
                'index_notice':request.POST.get('index_notice', None)
            }
        except Exception as E:

            log.error("信息POST不完整")

            return HttpResponse(json.dumps({
                'status': False,
                'error': '信息POST不完整'
            }))


        return HttpResponse(json.dumps(db.set_index(data)))


    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')



''' 设置用户个人站点信息

    /set_user_site/  post   方式

    参数  
        {
            blog_name 
            blog_info           // 没有参数就传 0
            blog_head_color 
            blog_bgm 
        }

    返回值 成功
    {
        'status':True,
    }
    
    失败
    
    {
        'status':False,
        'error':'xxxx'
    }
'''

@Auth.auth()
def set_user_site(request):

    if request.method == 'POST':

        try:
            data = {
                'blog_name':request.POST['blog_name'],
                'blog_info':request.POST['blog_info'],
                'blog_head_color':request.POST['blog_head_color'],
                'blog_bgm':request.POST['blog_bgm'],
            }
        except Exception as E:

            log.error("信息POST不完整")

            return HttpResponse(json.dumps({
                'status': False,
                'error': '信息POST不完整'
            }))



        return HttpResponse(json.dumps(db.set_user_site(request.session['user_name'],data)))


    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')

''' 修改用户密码或头像

    /set_user/  post  方式
    
    参数 {
        do:'re_passwd' or 're_head',
        old_passwd   # 旧密码
        new_passwd   # 新密码
        user_head    # 或者修改user_head
    }

    返回值 成功
    {
        'status':True,
    }

    失败

    {
        'status':False,
        'error':'xxxx'
    }
'''

@Auth.auth()
def set_user(request):

    if request.method == 'POST':

        t = Test(request, {'re_passwd': ['old_passwd','new_passwd'],
                           're_head': ['user_head']}
                 )

        if t['status'] == True:

            dic = t['dic']

            return HttpResponse(json.dumps(db.update_user(dic)))

        else:
            return HttpResponse(json.dumps(t))


    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')


''' 用户分类的管理器

    增 删 改 

    /class_manage/  post  方式

    参数 {
        'do':'del/update/add'
        'class_id':'1' //如果是add  不需要传入     update时需要传入 按照class_id 来更改class_name，class_id 本身不可以改变
        'class_name':'2'  //如果是del  不需要传入  update时需要传入
    }

    返回值 成功
    {
        'status':True,
    }

    失败

    {
        'status':False,
        'error':'xxxx'
    }
'''


@Auth.auth()
def class_manage(request):

    if request.method == 'POST':

        t = Test(request,{'del':['class_id'],
                          'add':['class_name'],
                          'update':['class_name','class_id']}
                 )

        if t['status'] == True:

            dic = t['dic']

        else:

            return  HttpResponse(json.dumps(t))

        return HttpResponse(json.dumps(db.class_manage(dic)))

    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')


''' 文章的管理器

    增 删 改 文章移动分类

    /article_manage/  post  方式

    参数 {
        'do':'del/update/add/move' // 如果是del    只需要 article_id
        'article_id':'1'           // 如果是add    不需要此参数
        'article_title':'123'      // 如果是move   不需要此参数
        'article_text':'xxx'       // 如果是move   不需要此参数
        'article_class_id':'123'   
    }

    返回值 成功
    {
        'status':True,
    }

    失败

    {
        'status':False,
        'error':'xxxx'
    }
'''

@Auth.auth()
def article_manage(request):

    if request.method == 'POST':

        t = Test(request, {
                    'add':['article_title','article_text','article_class_id'],
                    'update':['article_id','article_title','article_text','article_class_id'],
                    'move':['article_id','article_class_id'],
                    'del':['article_id']}
                 )


        if t['status'] == True:

            dic = t['dic']

        else:

            return HttpResponse(json.dumps(t))


        return HttpResponse(json.dumps(db.article_manage(dic)))

    else:

        log.error("错误的访问，无 GET")

        return HttpResponse('not get')

#----------------------------------------- 前端后台设置,需要权限 结束 ---------------------------------------------