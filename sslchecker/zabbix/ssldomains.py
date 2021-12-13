import json, os, logging, datetime
import mysql.connector


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
my_path = os.path.join(BASE_DIR, 'zabbix')

class SslMonitor():
    def toQueryDom(self):
        mydb = mysql.connector.connect(
          host="10.165.22.205",
          user="yrollrei",
          passwd="s22-C350",
          database="argus_v2"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT domain FROM SSLDOMAINS_ssldomain2 WHERE daysleft<20 AND skip='no'")
        b = mycursor.fetchall()
        d = {"data":[]}
        for new_b in b:
            d["data"].append({"{#DOMAINSSL}":new_b[0]})
        self.loggingFile(log_debug="{}".format("#####" * 20))
        self.loggingFile(log_debug="DOMAIN DISCOVER", log_info=json.dumps(d, indent=4))
        return json.dumps(d)


    def loggingFile(self, log_debug=None, log_info=None, log_warning=None, log_error=None, log_critical=None):
        logdir = os.path.join(my_path, 'logs/')
        logname = "ssldiscover"
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


if __name__=="__main__":
   a = SslMonitor()
   print(a.toQueryDom())


