from blog.models import *
from blog.helper.logHelper import logHelper
log = logHelper('log')
import json

'''
    UserSite
    Site
    Article
    ArticleClass
    User
'''



def get_user_list():

    ret = []

    user_list = User.objects.all()

    for item in user_list:
        ret.append({
            'user_id': item.id,
            'user_name':item.user_name,
        })



    return json.dumps(ret)

def site_info():


        obj = Site.objects.all()

        if obj:
            obj = obj[0]
            return json.dumps({

                'index_setting': obj.index_setting,
                'index_head_color': obj.index_head_color,
                'index_notice': obj.index_notice,

            })

        else:

            return json.dumps({
                'error':'后台无主页设置，请联系后台管理员'
            })



def get_article(article_id = False,user_id = False):

    ret = []

    if not user_id :

        article_list = Article.objects.filter(id = article_id)

    else:
        try:

            user_obj = User.objects.get(id = user_id)
            article_list = user_obj.user_article.all()

        except Exception as E:

            return json.dumps({
                'error':'您提供的用户有误，或者无此文章'
            })

    for item in article_list:

        ret.append(
            {
                "article_id":item.id,
                "article_title": item.article_title,
                "article_text":item.article_text,
                "article_date": item.article_date.strftime("%Y-%m-%d %H:%M:%S"),
                "article_modify_date": item.article_modify_date.strftime("%Y-%m-%d %H:%M:%S"),
                "article_pageviews": item.article_pageviews,
                "article_ding":item.article_ding,
                "article_class":item.article_class.class_name,
                "article_is_save": item.article_is_save,
            }
        )



    if user_id:
        return json.dumps(ret)
    else:
        return json.dumps(ret[0])


def get_user_setting(user_id):

    try :
        user_obj = User.objects.get(id = user_id)
        site_obj = user_obj.user_site
    except Exception as E:
        return {
            'error':'获取不到用户，请检查',
        }

    return json.dumps({
        'blog_name':site_obj.blog_name,
        'blog_info': site_obj.blog_info,
        'blog_head_color': site_obj.blog_head_color,
        'blog_bgm': site_obj.blog_bgm,

    })


def get_article_class(user_id = False):

    if user_id:
        try:
            user_obj = User.objects.get(id = user_id)

        except Exception as E:

            return json.dumps({
                'error':'请注意用户ID是否正确！'
            })

        article_class = user_obj.user_article_class.all()

    else:
        article_class = ArticleClass.objects.all()

    ret = []

    for item in article_class:
        ret.append({
            'class_id':item.id,
            'class_name':item.class_name
        })


    return json.dumps(ret)


def set_index(dic):

    try:
        site_obj = Site.objects.all()
    except Exception as E:
        log.w('获取主页设置数据错误！错误信息:%s' % E,'error')
        return {
            'status':False,
            'error' :'获取主页设置数据错误！错误信息:%s' % E
        }

    try:
        site_obj.update(**dic)
    except Exception as E:
        log.w('更新数据错误！错误信息:%s' % E, 'error')
        return {
            'status': False,
            'error': '更新数据错误！错误信息:%s' % E
        }

    log.w('更新数据成功', 'info')

    return {
        'status': True,
    }