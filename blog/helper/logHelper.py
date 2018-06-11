import logging
import sys,os

log = logging.getLogger('system')


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(2)
else:  # pragma: no cover
    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back

class logHelper():

    def __init__(self,log_name):


        if log_name:

            try:

                self.log = logging.getLogger(log_name)  # 参数是 定义好的 logger


            except Exception as E:

                log.error("log_name 参数错误,请检查,log 没有被正确初始化")

        else:

            log.error("log_name 参数为空,log没有被正确初始化")


    def findCaller(self, stack_info=False):

        f = currentframe()

        if f is not None:
            f = f.f_back
            rv = (f.f_code.co_filename, f.f_lineno, f.f_code.co_name)

        return rv


    def get_access_ip(self, request):

        if request.META.get('REMOTE_ADDR',False):
            return request.META['REMOTE_ADDR']
        else:
            log.warning('获取IP错误')
            return {
                "status":False,
                'error':'获取IP错误'
            }



    def w(self,note,level="info",ip = False):

        file_line = self.findCaller()
        file_line = "%s[line:%s]" % (file_line[0],file_line[1])

        LEVEL = [
            'debug',
            'info',
            'warning',
            'error',
            'critical',
        ]

        if level in LEVEL:

            try:

                w_log = getattr(self.log,level)

            except Exception as E:

                log.error("日志器选择LEVEL错误,请检查:%s",E)

                return {
                    'status': False,
                    'error': 'LEVEL 获取失败。请检查代码'
                }

        else:

            log.error('没有传输合适的LEVEL')
            return {
                'status':False,
                'error':'LEVEL 错误。请传输合适的参数，debug,info,warning,error,critical'
            }


        if note:

            if ip:
                temp_note = "%s %s %s" % (ip,file_line,note)
            else:
                temp_note = "%s %s"% (file_line,note)

            try:

                w_log(temp_note)

            except Exception as E:

                log.error("发生系统错误:%s",E)

        else:
            return {
                'status':False,
                'error':"请给予一个内容，蟹蟹！"
            }




