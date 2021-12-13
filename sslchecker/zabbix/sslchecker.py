from checker import *
import sys, os, logging, json
import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
my_path = os.path.join(BASE_DIR, 'zabbix')


def loggingFile(log_debug=None, log_info=None, log_warning=None, log_error=None, log_critical=None):
    logdir = os.path.join(my_path, 'logs/')
    logname = "sslchecker"
    os.popen("find {0} -type f -name '*.log' -mtime +30 -exec rm {1} \;".format(logdir, '{}'))
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename='{}{}-{}.log'.format(logdir, logname, datetime.datetime.now().strftime("%Y-%m-%d")),
        format=LOG_FORMAT, level=logging.DEBUG)
    logger = logging.getLogger()
    if log_debug:
        logger.debug(str(log_debug))
    if log_info:
        logger.info(str(log_info))
    if log_warning:
        logger.warning(str(log_warning))
    if log_error:
        logger.error(str(log_error))
    if log_critical:
        logger.critical(str(log_critical))


def checkeme(dom):
    try:
        expiration = sslchecker_notA(dom)
        date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
        get_exp = datetime.datetime.strftime(expiration, '%Y-%m-%d %H:%M:%S')
        rExp = datetime.datetime.strptime(get_exp, '%Y-%m-%d %H:%M:%S')

        daysleft = rExp - date_now
        #
        # print(dom)
        # print(expiration)
        # print(daysleft)
        loggingFile(log_debug="{}".format("#####" * 20))
        loggingFile(log_debug="DOMAIN INFO", log_info=json.dumps({"DOMAIN": dom, "EXPIRATION": str(expiration), "DAYS": str(daysleft)}, indent=4))

        return daysleft.days

    except Exception as e:
        domain = sslcheckercurl(dom)
        loggingFile(log_debug="{}".format("#####" * 20))
        loggingFile(log_debug="DOMAIN PYTHON ERROR",
                    log_info=json.dumps({"DOMAIN": dom, "PYTHON ERROR": str(e), "DOMAIN_CURL": domain}, indent=4))
        return domain



if __name__ == '__main__':
    print(int(checkeme(sys.argv[1])))

