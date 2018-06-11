from django.shortcuts import render,HttpResponse
from blog.Auth import Auth
from blog import dataHelper as db
import json
from blog.helper.logHelper import logHelper
log = logHelper('log')

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
            "status": true
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

            if Auth.is_login(user_name, user_passwd, request)['status']:

                log.w(("用户登录成功 USER_NAME:%s" % user_name), 'info', log.get_access_ip(request))

                return HttpResponse(json.dumps({
                    'status': True,
                }))

            else:

                log.w("用户名或密码错误", 'error', log.get_access_ip(request))

                return HttpResponse(json.dumps({
                    'status': False,
                    'error': '用户名或密码错误!'
                }))

        else:

            log.w("用户名密码为空", 'error', log.get_access_ip(request))

            return HttpResponse(json.dumps({
                'status': False,
                'error': '用户名密码为空!'
            }))

    else:

        log.w("错误的访问，无 GET", 'error', log.get_access_ip(request))

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

            log.w("用户注销成功", 'info', log.get_access_ip(request))

            return HttpResponse(json.dumps({
                'status': True
            }))

        else:

            log.w(("用户注销失败 错误信息:%s" % ret['error']), 'error', log.get_access_ip(request))

            return HttpResponse(json.dumps({
                'sataus': False,
                'error': ret['error']
            }))

    else:

        log.w("错误的访问，无 GET", 'error', log.get_access_ip(request))

        return HttpResponse('not get')


'''获取用户登录属性

    /get_login/  post 方式

        获取成功
        {
            "status": true
            "user_name": 'user_name'
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

            log.w("获取用户登录状态成功", 'info', log.get_access_ip(request))

            return HttpResponse(json.dumps(ret))

        else:

            log.w("获取用户登录状态失败", 'info', log.get_access_ip(request))

            return HttpResponse(json.dumps({
                'status': False
            }))

    else:

        log.w("错误的访问，无 POST", 'error', log.get_access_ip(request))

        return HttpResponse('not post')


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

        log.w("获取主页设置", 'info', log.get_access_ip(request))

        return HttpResponse(db.site_info())

    else:

        log.w("错误的访问，无 POST", 'error', log.get_access_ip(request))

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





    if request.method == 'GET':

        log.w('获取了全部用户列表', 'info', ip=log.get_access_ip(request))

        return HttpResponse(db.get_user_list())

    else:

        log.w("错误的访问，无 POST", 'error', log.get_access_ip(request))

        return HttpResponse('not post')


"""
    返回所有分类

    /get_user_list/  post 方式
    
    可传参数 user_id

    返回值
        [
            {
                "class_id": 1,
                "class_name": "HTML 分类"
            },
            {
                "class_id": 2,
                "class_name": "CSS 分类"
            },
            {
                "class_id": 3,
                "class_name": "Python 分类"
            },
            {
                "class_id": 4,
                "class_name": "Django 分类"
            }
        ]
"""


def get_article_class(request):

    if request.method == 'POST':

        if request.POST.get('user_id',False):

            user_id = request.POST['user_id']

            log.w(('获取用户文章分类USER_ID:%s' % user_id) ,'info',log.get_access_ip(request))

            return HttpResponse(db.get_article_class(user_id = user_id))

        else:

            log.w('获取所有用户文章分类','info', log.get_access_ip(request))

            return HttpResponse(db.get_article_class())
    else:

        log.w("错误的访问，无 GET", 'error', log.get_access_ip(request))

        return HttpResponse('not get')




'''
    /get_article/  post 方式
    参数 article_id 或者 user_id
    传递 user_id    返回 用户的所有文章
    传递 article_id 返回 单篇文章
    返回值(article_id 为参数)
        {
            "article_id": 1,
            "article_title": "你好",
            "article_text": "你好测试一下",
            "article_date": "2018-06-06 14:02:13",
            "article_modify_date": "2018-06-06 14:02:13",
            "article_pageviews": 1,
            "article_ding": 1
        }
    返回值(user_id 为参数)
        [
            {
                "article_id": 1,
                "article_title": "你好",
                "article_text": "你好测试一下",
                "article_date": "2018-06-06 14:02:13",
                "article_modify_date": "2018-06-06 14:02:13",
                "article_pageviews": 1,
                "article_ding": 1
            },
            {
                "article_id": 2,
                "article_title": "你好",
                "article_text": "测试你好",
                "article_date": "2018-06-06 14:45:23",
                "article_modify_date": "2018-06-06 14:45:23",
                "article_pageviews": 1,
                "article_ding": 2
            }
        ]
'''

def get_article(request):

    if request.method == 'POST':

        if request.POST.get('user_id',False):

            user_id = request.POST['user_id']

            log.w(('获取用户所有文章 USER_ID:%s' % user_id), 'info', log.get_access_ip(request))

            return HttpResponse(db.get_article(user_id = user_id))

        else:

            try:

                article_id = request.POST.get('article_id',False)

                log.w(('获取文章 ARTICLE_ID:%s' % article_id), 'info', log.get_access_ip(request))

                return HttpResponse(db.get_article(article_id))

            except Exception as E:

                log.w(("获取单个文章出错 错误信息:%s" % E),'error', log.get_access_ip(request))

                return HttpResponse(json.dumps({
                    'status':False,
                    'error':'获取单个文章出错，详细见日志'
                }))

    else:

        log.w("错误的访问，无 GET", 'error', log.get_access_ip(request))

        return HttpResponse("not get")



'''
    /get_user_site_setting/  post 方式
    参数 user_id

    返回值用户设置
        {
            "blog_info": "怕是个肥狗子哦！",
            "blog_bgm": null,
            "blog_head_color": "#545454",
            "blog_name": "huanghei"
        }
'''


def get_user_site_setting(request):

    if request.method == 'POST':

        if request.POST.get('user_id',False):

            user_id = request.POST['user_id']

            log.w(('获取用户设置 USER_ID:%s' % user_id), 'info', log.get_access_ip(request))

            return HttpResponse(db.get_user_setting(user_id))

        else:

            log.w('获取用户设置失败，因为没有USER_ID', 'error', log.get_access_ip(request))

            return HttpResponse(json.dumps({
                'status':False,
                'error':'请给我一个用户ID!'
            }))


    else:

        return HttpResponse('not get')

#----------------------------------------- 前端展示,无需权限 结束 ---------------------------------------------

#----------------------------------------- 前端后台设置,需要权限 开始 ---------------------------------------------



#----------------------------------------- 前端后台设置,需要权限 结束 ---------------------------------------------