from blog.helper.logHelper import logHelper
log = logHelper('log')

def Test(req,do_list):

    try:
        dic = {
            'do': req.POST['do'],
            'user_id': req.session['user_id']
        }
        print(dic,list(do_list.keys()))
        if dic['do'] not in list(do_list.keys()):

            log.w("do 错误", 'error', log.get_access_ip(req))

            return {
                'status': False,
                'error': 'do 错误'
            }

    except Exception as E:

        log.w("没有do，不知道如何操作", 'error', log.get_access_ip(req))

        return {
            'status': False,
            'error': '没有do，不知道如何操作'
        }

    try:

        for keys in do_list[dic['do']]:

            dic[keys] = req.POST[keys]

    except Exception as E:

        log.w('POST信息不完整', 'error', log.get_access_ip(req))

        return {
            'status': False,
            'error': 'POST信息不完整'
        }


    return {
        'status': True,
        'dic': dic
    }