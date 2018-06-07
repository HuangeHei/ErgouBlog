from blog.models import *
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

    '''
        user_name = models.CharField(max_length=1024,null=False,blank=False)      # 用户名
        user_passwd = models.CharField(max_length=1024, null=False, blank=False)  # 用户密码
        user_head  = models.CharField(max_length=1024,null=False,blank=False)     # 用户 head 头
        user_article = models.ManyToManyField(Article)                            # 用户文章
        user_article_class = models.ManyToManyField(ArticleClass)                 # 用户文章分类
        user_site = models.ForeignKey(UserSite,on_delete=models.CASCADE)          # 用户主页设置
    '''

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
                "article_ding":item.article_ding
            }
        )



    if user_id:
        return json.dumps(ret)
    else:
        return json.dumps(ret[0])

    '''
        article_title = models.CharField(max_length=200,null=False,blank=False)   # 文章标题
        article_text = models.TextField()                                         # 文章内容
        article_date = models.DateTimeField(auto_now_add=True)                    # 文章初始日期
        article_modify_date = models.DateTimeField(auto_now_add=True)             # 文章修改日期
        article_pageviews = models.IntegerField(default=0)                        # 文章阅读量
        article_ding = models.IntegerField(default=0)    
    '''


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

    '''
        blog_name = models.CharField(max_length=30,null=False,blank=False)                           # 用户博客名称
        blog_info = models.CharField(max_length=80,null=False,blank=False,default="怕是个肥狗子哦！")  # 用户博客简介
        blog_head_color = models.CharField(max_length=10,null=False,blank=False,default='#545454')   # 用户头颜色
        blog_bgm = models.CharField(max_length=100,null=True,blank=True)                             # 用户博客BGM
    '''