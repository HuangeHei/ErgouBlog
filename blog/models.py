from django.db import models

# Create your models here.


from django.db import models

# Create your models here.

class UserSite(models.Model):

    blog_name = models.CharField(max_length=30,null=False,blank=False)                           # 用户博客名称
    blog_info = models.CharField(max_length=80,null=False,blank=False,default="怕是个肥狗子哦！")  # 用户博客简介
    blog_head_color = models.CharField(max_length=10,null=False,blank=False,default='#545454')   # 用户头颜色
    blog_bgm = models.CharField(max_length=100,null=True,blank=True)                             # 用户博客BGM

    def __str__(self):
        return self.blog_name


class Site(models.Model):

    index_setting = models.CharField(max_length=1024,null=True,blank=True)                       # setting
    index_head_color = models.CharField(max_length=10,null=False,blank=False,default='#545454')  # index head
    index_notice = models.CharField(max_length=1024,null=True,blank=True)                        # 公告

    def __str__(self):
        return self.index_setting


class Article(models.Model):

    article_title = models.CharField(max_length=200,null=False,blank=False)   # 文章标题
    article_text = models.TextField()                                         # 文章内容
    article_date = models.DateTimeField(auto_now_add=True)                    # 文章初始日期
    article_modify_date = models.DateTimeField(auto_now_add=True)             # 文章修改日期
    article_pageviews = models.IntegerField(default=0)                        # 文章阅读量
    article_ding = models.IntegerField(default=0)                             # 文章点赞量

    def __str__(self):
        return self.article_title



class ArticleClass(models.Model):

    class_name = models.CharField(max_length=200)                             # 类别名称
    class_article = models.ManyToManyField(Article)                           # 类别内文章

    def __str__(self):
        return self.class_name



class User(models.Model):

    user_name = models.CharField(max_length=1024,null=False,blank=False)      # 用户名
    user_passwd = models.CharField(max_length=1024, null=False, blank=False)  # 用户密码
    user_head  = models.CharField(max_length=1024,null=False,blank=False)     # 用户 head 头
    user_article = models.ManyToManyField(Article)                            # 用户文章
    user_article_class = models.ManyToManyField(ArticleClass)                 # 用户文章分类
    user_site = models.ForeignKey(UserSite,on_delete=models.CASCADE)          # 用户主页设置


    def __str__(self):
        return self.user_name






