from blog.models import User
from django.shortcuts import render,HttpResponse
from blog.helper.logHelper import logHelper
import json
log_system = logHelper('system')
log_server = logHelper('log')



class Auth():

    @classmethod
    def login_status(cls,req):

        if  req.session.get('user_id',False) and (req.session.get('status',False) == True):
            return {
                'status':True,
                'user_name':req.session['user_name'],
                'user_id': req.session['user_id']
            }
        else:
            req.session.delete()
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

                req.session['user_id'] = user_obj.id           # user_id
                req.session['user_name'] = user_obj.user_name  # user_name
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

            req.session.delete()

            #if not cls.login_status(req)['status']:

            return {
                'status':True,
            }

        else:
            return {
                'status':False,
                'error':'并没有登录!'
            }

    @classmethod
    def auth(cls):

        def outer_wrapper(func):

            def wap(*args, **kwargs):

                request = args[0]  # request

                if Auth.login_status(request)['status']:

                    try:

                        obj = User.objects.get(id = request.session['user_id'])

                    except Exception as e:

                        log_server.w('用户不存在 进入用户%s' % request.session['user_name'] ,'error',request)

                        return HttpResponse(json.dumps({
                            'status':False,
                            'error':'用户不存在'
                        }))


                    return func(*args, **kwargs)  # 执行函数

                else:

                    return HttpResponse(json.dumps({
                        'status':False,
                        'error':'用户没有登录'
                    }))

            return wap

        return outer_wrapper






