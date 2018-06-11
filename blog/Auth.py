from blog.models import User,Auth
from django.shortcuts import render,HttpResponse
from blog.helper.logHelper import logHelper
log_system = logHelper('system')
log_server = logHelper('log')
class Auth():

    @classmethod
    def login_status(cls,req):

        if  req.session.get('user_name',False) and (req.session.get('status',False) == True):
            return {
                'status':True,
                'user_name':req.session['user_name']
            }
        elif req.session.get('user_name',False):
            req.session.delete()
            return {
                'status':False
            }
        else:
            return {
                'status':False
            }

    @classmethod
    def is_login(cls,user_name,passwd,req):

        if user_name and passwd:

            try:
                user_obj = User.objects.get(user_name = user_name,user_passwd = passwd)

            except Exception as E:

                return {
                    'status':False,
                    'error':'账号或密码错误!'
                }


            if cls.login_status(req)['status']:# 检查后台session是否设置了

                return {
                    'status':True
                }
            else:

                req.session['user_name'] = user_obj.user_name
                req.session['status'] = True
                return {
                    'status': True
                }
        else:

            return {
                'status':False,
                'error':'账号或密码为空!'
            }

    @classmethod
    def out_login(cls,req):
        ret_buf = cls.login_status(req)
        if ret_buf['status']:

            req.session.delete() # 进行注销

            if not cls.login_status(req)['status']:

                return {
                    'status':True,
                }

        else:
            return {
                'status':False,
                'error':'并没有登录!'
            }

    @classmethod
    def auth(cls,root):

        def outer_wrapper(func):
            def wap(*args, **kwargs):

                try:

                    root_obj = Auth.objects.get(root_name = root)  # 这一步主要怕蠢萌程序员

                except Exception as E:

                    print('程序内部')  # 内部报错信息 以后写入到日志系统中
                    return HttpResponse('程序内部发生问题')

                if cls.is_login(args[1]):

                    try:

                        obj = User.objects.get(user_name=args[1].session['user_name'])

                        try:
                            is_ok = obj.user_root.filter(root_name=root_obj.root_name)

                        except Exception as e:

                            return HttpResponse('用户权限获取失败')

                    except Exception as e:

                        return HttpResponse('not,用户不存在')

                    if is_ok:

                        return func(*args, **kwargs)  # 执行函数

                    else:

                        return HttpResponse('not,无权限')

                else:

                    return HttpResponse('not,没有登录')

            return wap

        return outer_wrapper






