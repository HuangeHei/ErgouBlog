from blog.models import User


class Auth():

    @classmethod
    def login_status(cls,req):

        if  req.session.get('user_name',False) and (req.session.get('user_name',False) == True):
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
        if ret_buf.status:

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







