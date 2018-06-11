"""
Django settings for EgouBlog project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9%%f+swemuc-fq+^!z!#3)2o8or7o4yt!x4ick0o_n0_4_0o+r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EgouBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'EgouBlog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/


LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# session 关闭即过期

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# 日志配置

''' 日志等级分类

    DEBUG：用于调试目的的底层系统信息
    INFO：普通的系统信息
    WARNING：表示出现一个较小的问题。
    ERROR：表示出现一个较大的问题。
    CRITICAL：表示出现一个致命的问题。

'''




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)-8s %(pathname)s[line:%(lineno)d] %(message)s'
            # 'format': '%(asctime)s %(levelname)-8s %(pathname)s[line:%(lineno)d] %(message)s'
        },
        'my_logHelper': {
            'format': '%(asctime)s %(levelname)-8s %(message)s'
            #'format': '%(asctime)s %(levelname)-8s %(pathname)s[line:%(lineno)d] %(message)s'
        },
        'request': {
            'format': '%(asctime)s %(levelname)-8s %(pathname)s[line:%(lineno)d] %(message)s'
            # 'format': '%(asctime)s %(levelname)-8s %(pathname)s[line:%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',                                  # 日志分发级别
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 日志分发方式或日志切割方式
            'filename': './log/info.log',
           #'maxBytes': 1024 * 1024 * 5,                      # 5 MB
            'when':'D',
            'backupCount': 100,
            'formatter': 'my_logHelper',
            'encoding':'utf-8'
        },
        'files': {
            'level': 'WARNING',                                    # 日志分发级别
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 日志分发方式或日志切割方式
            'filename': './log/warning.log',
           # 'maxBytes': 1024 * 1024 * 5,                          # 5 MB
            'when':'D',
            'backupCount': 100,
            'formatter': 'my_logHelper',
            'encoding':'utf-8'
        },
        'request': {
            'level': 'INFO',                                       # 日志分发级别
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 日志分发方式或日志切割方式
            'filename': './log/request.log',
           # 'maxBytes': 1024 * 1024 * 5,                          # 5 MB
            'when':'D',                                            # 一天一日志
            'backupCount': 100,
            'formatter': 'request',
            'encoding':'utf-8'
        },
        'request_warning': {
            'level': 'WARNING',                                    # 日志分发级别
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 日志分发方式或日志切割方式
            'filename': './log/request_warning.log',               # 一天一日志
           # 'maxBytes': 1024 * 1024 * 5,                          # 5 MB
            'when':'D',
            'backupCount': 100,
            'formatter': 'request',
            'encoding':'utf-8'
        },
        'system': {
            'level': 'WARNING',  # 日志分发级别
            'class': 'logging.handlers.TimedRotatingFileHandler',   # 日志分发方式或日志切割方式
            'filename': './system.log',                # 系统错误，请移交到别的盘
            # 'maxBytes': 1024 * 1024 * 5,                          # 5 MB
            'when': 'D',
            'backupCount': 100,
            'formatter': 'default',
            'encoding':'utf-8'

        },
    },
    'loggers': {
        'log': {
            'handlers': ['file','files'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['request','request_warning'],
            'level': 'INFO',
            'propagate': True,
        },
        'system': {
            'handlers': ['system'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


