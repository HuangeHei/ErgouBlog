from django.shortcuts import render,HttpResponse
from blog.Auth import Auth
from blog import dataHelper as db
import json
import logging
log = logging.getLogger(__name__)


# Create your views here.

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
        return HttpResponse(db.site_info())
    else:
        return HttpResponse('not post')

def get_user(request):

    return HttpResponse(db.get_user_list())

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

        return HttpResponse(db.get_user_list())

    else:

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
            return HttpResponse(db.get_article_class(user_id = request.POST['user_id']))
        else:
            return HttpResponse(db.get_article_class())
    else:
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

            return HttpResponse(db.get_article(user_id = user_id))

        else:

            try:

                article_id = request.POST.get('article_id',False)

                return HttpResponse(db.get_article(article_id))

            except Exception as E:

                return HttpResponse(json.dumps('cuole'))

    else:

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

            return HttpResponse(db.get_user_setting(request.POST['user_id']))

        else:

            return HttpResponse(json.dumps({
                'error':'请给我一个用户ID!'
            }))


    else:

        return HttpResponse('not get')



def login(request):

    if request.method == 'POST':

        user_name = request.POST.get('user_name',False)
        user_passwd = request.POST.get('user_passwd',False)

        if user_name and user_passwd:
            print(user_name,user_passwd)
            if Auth.is_login(user_name,user_passwd,request)['status']:
                log.info("用户尝试登陆 登录名:%s" % user_name)
                return HttpResponse(json.dumps({
                    'status': True,
                }))
            else:
                return HttpResponse(json.dumps({
                    'status': False,
                    'error': '用户名或密码错误!'
                }))

        else:
            return HttpResponse(json.dumps({
                'status':False,
                'error':'用户名密码为空!'
            }))
    else:
        return HttpResponse('not get')


def out(request):

    if request.method == 'POST':

        ret = Auth.out_login(request)

        if ret['status']:
            return HttpResponse(json.dumps({
                'status':True
            }))
        else:
            return HttpResponse(json.dumps({
                'sataus':False,
                'error':ret['error']
            }))

    else:

        return HttpResponse('not get')


def get_login_status(request):


    if request.method == 'GET':

        ret = Auth.login_status(request)

        if ret['status']:
            return HttpResponse(json.dumps(ret))
        else:
            return HttpResponse(json.dumps({
                'status': False
            }))

    else:

        return HttpResponse('not post')








