from django.shortcuts import render,HttpResponse
from blog import dataHelper as db
import json

# Create your views here.

"""
    返回
    
    /get_index_setting/  get 方式
    
    返回值
        {
            "index_setting": "随便写",
            "index_head_color": "#545454",
            "index_notice": "我是来逗比的公告~"
        }
"""
def get_index_setting(request):

    return HttpResponse(db.site_info())

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

    return HttpResponse(db.get_user_list())

def article_class(request):
    pass


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

def get_user_site_setting(request):

    pass

def get_user_article_title_id(request):

    pass









