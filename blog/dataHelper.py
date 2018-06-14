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
        user_obj = {'user_name':'all'}
        article_class = ArticleClass.objects.all()

    ret = []

    for item in article_class:
        ret.append({
            'class_id':item.id,
            'class_name':item.class_name,
            'user':user_obj.user_name
        })


    return json.dumps(ret)


def set_index(dic):

    try:
        site_obj = Site.objects.all()
    except Exception as E:
        log.w('主页设置数据错误！错误信息:%s' % E,'error')
        return {
            'status':False,
            'error' :'主页设置数据错误！错误信息:%s' % E
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

def set_user_site(user,dic):

    try:
        obj = UserSite.objects.filter(User__user_name = user)

    except Exception as E:

        log.w('查询用户错误！错误信息:%s' % E,'error')

        return {
            'status':False,
            'error' :'查询用户错误！错误信息:%s' % E
        }

    try:

        obj.update(**dic)

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


def update_user(user_name,user_passwd = None,user_head = None):

    obj = User.objects.filter(user_name=user_name)

    if obj:

        try:
            if user_passwd is not None:

                obj.update(user_passwd = user_passwd)

            elif user_head is not None:

                obj.update(user_head = user_head)

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

    else:

        log.w('更新数据错误！找不到用户' 'error')

        return json.dumps({
            'status':False,
            'error':'找不到用户！'
        })


def class_manage(dic):

    user_obj = User.objects.filter(user_name = dic['user_name'])

    try:
        if dic['do'] == 'add':

            if len(ArticleClass.objects.filter(class_name = dic['class_name'],User__user_name = dic['user_name'])) == 0:
                class_obj = ArticleClass.objects.create(class_name = dic['class_name'])
                user_obj[0].user_article_class.add(class_obj)

                log.w('添加成功', 'info')
                return {
                    'status': True,
                }
            else:
                log.w('添加失败', 'error')
                return {
                    'status': False,
                    'error':'分类命名重复'
                }



        elif dic['do'] == 'update':

            ArticleClass.objects.filter(id = dic['class_id']).update(class_name = dic['class_name'])

            log.w('更新成功', 'info')
            return {
                'status': True,
            }

        elif dic['do'] == 'del':

            class_obj = ArticleClass.objects.get(id = dic['class_id'])

            article = Article.objects.filter(article_class = class_obj)

            if len(article) == 0:

                class_obj.delete()

                log.w('删除成功！', 'info')
                return {
                    'status': True,
                }

            else:

                log.w('分类中还有文章无法删除！','error')
                return {
                    'status': False,
                    'error': '分类中还有文章无法删除！'
                }
        else:

            log.w("请传入正确的do参数", 'error')

            return {
                'status': False,
                'error': '请传入正确的do参数'
            }

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

'''
    else:

        log.w('更新数据错误！找不到用户' 'error')

        return json.dumps({
            'status':False,
            'error':'找不到用户！'
        })'''


def article_manage(dic):

    user_obj = User.objects.filter(user_name = dic['user_name'])

    try:

        class_obj = ArticleClass.objects.get(id=dic['article_class_id'],User__user_name = dic['user_name'])

    except Exception as E:

        log.w('无法获取文章分类 错误信息%s' % E, 'error')
        return {
            'status': False,
            'error': '无法获取文章分类 错误信息%s' % E
        }

    try:
        if dic['do'] == 'add':

            article_obj = Article.objects.create(article_title = dic['article_title'],
                                               article_text = dic['article_text'],
                                               article_class= class_obj,
                                               )
            user_obj[0].user_article.add(article_obj)

            log.w('添加文章成功', 'info')
            return {
                'status': True,
            }

        elif dic['do'] == 'update':

            article_obj = Article.objects.filter(id = dic['article_id'],User__user_name = dic['user_name'])

            if len(article_obj) == 0:

                log.w('无法获取文章！', 'error')

                return {
                    'status': False,
                    'error':'无法获取文章！'
                }
            else:

                article_obj.update(
                    article_title = dic['article_title'],
                    article_text = dic['article_text'],
                    article_class = class_obj,
                )

                log.w('更新成功', 'info')
                return {
                    'status': True,
                }

        elif dic['do'] == 'del':

            article_obj = Article.objects.filter(id = dic['article_id'], User__user_name = dic['user_name'])

            if len(article_obj) != 0:

                article_obj.delete()

                log.w('删除成功！', 'info')
                return {
                    'status': True,
                }

            else:

                log.w('无法获取文章！', 'error')

                return {
                    'status': False,
                    'error': '无法获取文章！'
                }
        elif dic['do'] == 'move':

            article_obj = Article.objects.filter(id = dic['article_id'], User__user_name = dic['user_name'])

            if len(article_obj) != 0:


                try:

                    article_obj.update(article_class = class_obj)

                except Exception as E:

                    log.w('文章移动分类失败 错误:%s'% E, 'error')

                    return {
                        'status': False,
                        'error': '文章移动分类失败'
                    }


                log.w('文章移动分类成功', 'info')
                return {
                    'status': True,
                }

            else:

                log.w('无法获取文章！', 'error')

                return {
                    'status': False,
                    'error': '无法获取文章！'
                }

        else:

            log.w("请传入正确的do参数", 'error')

            return {
                'status': False,
                'error': '请传入正确的do参数'
            }

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


