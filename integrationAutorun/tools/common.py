import subprocess
import logging
from constant import *

logger_name = ''


def register_logger_name(_logger_name):
    global logger_name
    logger_name = _logger_name


def contain_string(files, string):
    rtn = False
    try:
        f = open(files, 'r')
        try:
            lines = f.readlines()
            for line in lines:
                if string in line:
                    rtn = True
        finally:
            f.close()
    except Exception as e:
        print(files, e)

    return rtn


def execute(cmd):
    # prc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # return prc.communicate()[0]
    return_code = subprocess.call(cmd, shell=True)
    logging.getLogger(logger_name).info("===== run command : %s " % cmd)
    # print cmd + ' return result : ' + str(return_code)
    return return_code
