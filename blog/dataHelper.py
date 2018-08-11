from blog.models import *
from django.db.models import Q
from blog.Auth import Auth
import json
import logging


log = logging.getLogger('system')

'''
    UserSite
    Site
    Article
    ArticleClass
    User
'''
def create(user_info):
    '''
    :param
        user_name:'ccc'
        user_passwd:'ccc'
    :return: True and False
    '''
    create_ret = Auth.create_user(User,user_info)

    if create_ret['status'] :
        ret_user = create_ret['model']
        try:
            def_user_site = UserSite.objects.create(blog_name = '%s的博客' % user_info['user_name'],
                                                    blog_info = '还没有博客简介哦~')

            ret_user.user_site = def_user_site  # 更新

            def_category = ArticleClass.objects.create(class_name = '%s的默认分类' % user_info['user_name'])

            def_article = Article.objects.create(article_title = '第一个文章哦',
                                                 article_text = '这是你的第一篇文章哦~要加油~',
                                                 article_class = def_category
                                                 )

            ret_user.user_article.add(def_article)
            ret_user.user_article_class.add(def_category)

            ret_user.save()

        except Exception as E:

            log.error('%s用户添加失败,错误信息:%s' % (user_info['user_name'],E))

            return False

        return True

    else:
        return False


def ret_article(ret_list):

    if len(ret_list) != 0:

        ret = []

        for item in ret_list:
            user = item.User.all()[0]
            ret.append(
                {
                    "article_id": item.id,
                    "article_title": item.article_title,
                    "article_text": item.article_text,
                    "article_date": item.article_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "article_modify_date": item.article_modify_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "article_pageviews": item.article_pageviews,
                    "article_ding": item.article_ding,
                    "article_class": item.article_class.class_name,
                    "article_class_id": item.article_class.id,
                    "user_name": user.user_name,
                    "user_id": user.id,
                    "article_is_save": item.article_is_save,
                }
            )

        return ret
    else:
        return False





def search(search_text):



    ret_list = Article.objects.filter(Q(article_title__icontains = search_text)|Q(article_text__icontains = search_text))

    ret = ret_article(ret_list)

    if ret:
        return ret

    else:
        return {
            'status':False,
            'error':'搜索不到您要的内容哦~'
        }



def get_user_list(user_id):

    ret = []
    if not user_id:
        user_list = User.objects.all()
    else:
        user_list = User.objects.filter(id = user_id)
    
    if len(user_list) != 0 :
        
        for item in user_list:
            ret.append({
                'user_id': item.id,
                'user_name':item.user_name,
                'user_head':item.user_head
            })
    else:
        
        ret = {
            'status':False,
            'error':'错误无用户或提供的user_id 不正确'
        }


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

    if article_id :

        article_list = Article.objects.filter(id = article_id)

    elif user_id:

        try:

            user_obj = User.objects.get(id = user_id)
            article_list = user_obj.user_article.all()

        except Exception as E:

            return json.dumps({
                'error':'您提供的用户有误，或者无此文章'
            })
    else:

        try:

            article_list = Article.objects.all()

        except Exception as E:

            return json.dumps({
                'error':'无法获取所有文章'
            })

    ret = ret_article(article_list)

    if ret:

        log.info('获取文章成功')

        if user_id:

            return json.dumps(ret)

        elif article_id:

            return json.dumps(ret[0])

        else:

            return json.dumps(ret)

    else:

        return json.dumps({
            'status': False,
            'error': 'ret_article 函数发生错误(程序判断为没有此文章)'
        })

        log.error('ret_article 函数发生错误')


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
        user = item.User.all()[0]
        ret.append({
            'class_id':item.id,
            'class_name':item.class_name,
            'user_id': user.id,
            'user_name':user.user_name,
        })

    return json.dumps(ret)


def set_index(dic):

    try:
        site_obj = Site.objects.all()
    except Exception as E:
        log.error('主页设置数据错误！错误信息:%s' % E)
        return {
            'status':False,
            'error' :'主页设置数据错误！错误信息:%s' % E
        }

    try:
        site_obj.update(**dic)
    except Exception as E:
        log.error('更新数据错误！错误信息:%s' % E)
        return {
            'status': False,
            'error': '更新数据错误！错误信息:%s' % E
        }

    log.info('更新数据成功')

    return {
        'status': True,
    }

def set_user_site(user,dic):

    try:
        obj = UserSite.objects.filter(User__user_name = user)

    except Exception as E:

        log.error('查询用户错误！错误信息:%s' % E)

        return {
            'status':False,
            'error' :'查询用户错误！错误信息:%s' % E
        }

    try:

        obj.update(**dic)

    except Exception as E:

        log.error('更新数据错误！错误信息:%s' % E)
        return {
            'status': False,
            'error': '更新数据错误！错误信息:%s' % E
        }

    log.info('更新数据成功')

    return {
        'status': True,
    }


def update_user(dic):

    obj = User.objects.get(id = dic['user_id'])

    if obj:
        if dic['do'] ==  're_passwd':

            return Auth.re_passwd(obj,dic['old_passwd'],dic['new_passwd'])

        elif dic['do'] == 're_head':

            if len(dic['user_head']) != 0:
                obj.user_head = dic['user_head']
                obj.save()
                return {
                    'status': True,
                }
            else:
                return {
                    'status':False,
                    'error':'头像为空'
                }


        '''
        try:
            if user_passwd is not None:

                Auth.re_passwd(obj,old_passwd,new_passwd)

            elif user_head is not None:

                obj.update(user_head = user_head)

        except Exception as E:

            log.error('更新数据错误！错误信息:%s' % E)
            return {
                'status': False,
                'error': '更新数据错误！错误信息:%s' % E
            }

        log.info('更新数据成功')

        return {
            'status': True,
        }'''

    else:

        log.error('更新数据错误！找不到用户')

        return json.dumps({
            'status':False,
            'error':'找不到用户！'
        })


def class_manage(dic):

    user_obj = User.objects.filter(id = dic['user_id']) # 找到当前用户

    if dic['do'] == 'add':

        if len(ArticleClass.objects.filter(class_name = dic['class_name'],User__id = dic['user_id'])) == 0:

            class_obj = ArticleClass.objects.create(class_name = dic['class_name']) # 创建class
            user_obj[0].user_article_class.add(class_obj)

            log.info('添加成功')
            return {
                'status': True,
            }
        else:
            log.error('添加失败')
            return {
                'status': False,
                'error':'分类命名重复'
            }

    elif dic['do'] == 'update':


        class_ret = ArticleClass.objects.filter(id = dic['class_id'],User__id = dic['user_id'])

        if len(class_ret):

            class_ret.update(class_name = dic['class_name'])

            log.info('更新成功')
            return {
                'status': True,
            }

        else:

            log.error('更新失败')
            return {
                'status': False,
                'error':'当前登录的用户与分类所属用户不符合'
            }


    elif dic['do'] == 'del':

        class_obj = ArticleClass.objects.get(id = dic['class_id'])

        article = Article.objects.filter(article_class = class_obj)

        if len(article) == 0:

            class_obj.delete()

            log.info('删除成功！')
            return {
                'status': True,
            }

        else:

            log.error('分类中还有文章无法删除！')
            return {
                'status': False,
                'error': '分类中还有文章无法删除！'
            }
    else:

        log.error("请传入正确的do参数")

        return {
            'status': False,
            'error': '请传入正确的do参数'
        }

    log.info('更新数据成功')

    return {
        'status': True,
    }


def article_manage(dic):

    user_obj = User.objects.filter(id = dic['user_id'])

    if dic['do'] not in ['del']:

        try:

            class_obj = ArticleClass.objects.get(id=dic['article_class_id'], User__id=dic['user_id'])

        except Exception as E:

            log.error('无法获取文章分类 错误信息%s' % E)
            return {
                'status': False,
                'error': '无法获取文章分类 错误信息%s,如果你是update那么可能是目标分类不属于你' % E
            }

    try:
        if dic['do'] == 'add':

            article_obj = Article.objects.create(article_title = dic['article_title'],
                                               article_text = dic['article_text'],
                                               article_class= class_obj,
                                               )
            user_obj[0].user_article.add(article_obj)

            log.info('添加文章成功')
            return {
                'status': True,
            }

        elif dic['do'] == 'update':

            article_obj = Article.objects.filter(id = dic['article_id'],User__id = dic['user_id'])

            if len(article_obj) == 0:

                log.error('无法获取文章！')

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

                log.info('更新成功')
                return {
                    'status': True,
                }

        elif dic['do'] == 'del':

            article_obj = Article.objects.filter(id = dic['article_id'],User__id = dic['user_id'])

            if len(article_obj) != 0:

                article_obj.delete()

                log.info('删除成功！')
                return {
                    'status': True,
                }

            else:

                log.error('无法获取文章！')

                return {
                    'status': False,
                    'error': '无法获取文章！'
                }

        elif dic['do'] == 'move':

            article_obj = Article.objects.filter(id = dic['article_id'], User__id = dic['user_id'])

            if len(article_obj) != 0:

                article_obj.update(article_class = class_obj)

                log.info('文章移动分类成功')
                return {
                    'status': True,
                }

            else:

                log.error('无法获取文章！')

                return {
                    'status': False,
                    'error': '无法获取文章！'
                }
    except Exception as E:

        log.error('更新错误 错误信息:%s' % E)

        return {
            'status': False,
            'error': '更新错误 错误信息:%s' % E
        }
