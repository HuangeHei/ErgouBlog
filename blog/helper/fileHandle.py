import os
import sys
from blog.helper.logHelper import logHelper
from shutil import copy
log = logHelper('log')

def remove_file(path,filelist):

    for file in filelist:
        try:
            os.remove(os.path.join(path, file))

        except FileNotFoundError as e:
            log.w('未能找到文件','error')
            return False
        except Exception as E:
            log.w('未知错误:%s'% E ,'error')
            return False

    return True


def mv_img(_from,_to,filelist):
    '''
    list - mv file
    :param path:  temp dir path
    :param filelist: file_name_list
    :return: true and false
    '''

    for file in filelist:
        try:

            copy(os.path.join(_from, file),os.path.join(_to, file))

        except FileNotFoundError as E:
            log.w('未能找到文件', 'error')
            return False
        except Exception as E:
            log.w('未知错误:%s' % E, 'error')
            return False

    if remove_file(_from,filelist):
        return True
    else:
        return False