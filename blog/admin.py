from django.contrib import admin

# Register your models here.
from blog.models import *
# Register your models here.

admin.site.register(UserSite)
admin.site.register(Site)
admin.site.register(Article)
admin.site.register(ArticleClass)
admin.site.register(User)

