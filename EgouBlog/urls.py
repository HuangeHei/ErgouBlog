"""EgouBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views as blog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_user_list/', blog.get_user_list),
    path('get_index_setting/', blog.get_index_setting),
    path('get_article/', blog.get_article),
    path('get_user_site_setting/', blog.get_user_site_setting),
    path('get_article_class/', blog.get_article_class),
    path('login/', blog.login),
    path('out/', blog.out),
    path('get_login/', blog.get_login_status),
]
