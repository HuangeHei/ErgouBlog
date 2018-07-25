


def get_access_ip(self, request):
    if request.META.get('REMOTE_ADDR', False):
        return request.META['REMOTE_ADDR']
    else:

        return {
            "status": False,
            'error': '获取IP错误'
        }




