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

    obj = Site.objects.get(id=1)

    return json.dumps({

        'index_setting':obj.index_setting,
        'index_head_color':obj.index_head_color,
        'index_notice':obj.index_notice,

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

            return '您提供的user有误，或者无此文章 错误信息:%s' % E

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