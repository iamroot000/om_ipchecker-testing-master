import json, datetime, logging, os, sys, mysql.connector











class DomainDNS():

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.my_path = os.path.join(BASE_DIR, 'greatwallLOL')

        secretfile = os.path.join(self.my_path, '.secret.json')

        data = open(secretfile, 'r')

        data = json.load(data)

        host = data["host"]

        user = data["user"]

        passwd = data["password"]

        database = data["database"]

        self.result_name = "result"

        self.domain_field = 1

        self.idc_field = 2

        self.china_field = 3

        self.result_field = 4

        self.table = 'dnschina_checker'

        self.column = "*"

        try:

            self.mydb = mysql.connector.connect(

                host=host,

                user=user,

                passwd=passwd,

                database=database

            )

        except Exception as e:

            self.loggingFile(log_debug="{}".format("#####" * 20))

            self.loggingFile(log_debug="MySQL Query Error", log_error=str(e))







    def loggingFile(self, log_debug=None, log_info=None, log_warning=None, log_error=None, log_critical=None):

        logdir = os.path.join(self.my_path, 'logs/')

        os.popen("find {0} -type f -name '*.log' -mtime +40 -exec rm {1} \;".format(logdir, '{}'))

        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

        logging.basicConfig(

            filename='{}{}-{}.log'.format(logdir, self.table,datetime.datetime.now().strftime("%Y-%m-%d-%H")),

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











    def mysqlQuery(self):

        mycursor = self.mydb.cursor()

        mycursor.execute("SELECT {} FROM {}".format(self.column, self.table))

        data = mycursor.fetchall()

        self.loggingFile(log_debug="{}".format("#####" * 20))

        self.loggingFile(log_debug="MySQL Query", log_info=data)

        return data





    def mysqlEdit(self):

        dbdata = self.mysqlQuery()

        for i in dbdata:

            mycursor = self.mydb.cursor()

            if i[self.china_field] == 'error' or i[self.idc_field] == 'error':

                sql = "UPDATE {} SET {} = %s WHERE {} = %s".format(self.table, self.result_name, i[0])

                val = (2, i[0])

                self.loggingFile(log_debug="{}".format("#####" * 20))

                self.loggingFile(log_debug="MySQL Output Error", log_warning=i)

                self.loggingFile(log_debug="{}".format("-----" * 20))

                self.loggingFile(log_debug="MySQL Output Error info", log_warning="id={}, idc={}, china={}".format(i[0], i[self.dns_field], i[self.china_field]))

                mycursor.execute(sql, val)

            elif i[self.idc_field] != i[self.china_field]:

                sql = "UPDATE {} SET {} = %s WHERE {} = %s".format(self.table, self.result_name, i[0])

                val = (1, i[0])

                self.loggingFile(log_debug="{}".format("#####" * 20))

                self.loggingFile(log_debug="MySQL Output Not Equal", log_error=i)

                self.loggingFile(log_debug="{}".format("-----" * 20))

                self.loggingFile(log_debug="MySQL Output Not Equal info", log_error="id={}, idc={}, china={}".format(i[0], i[self.dns_field], i[self.china_field]))

                mycursor.execute(sql, val)

            elif i[self.idc_field] == i[self.china_field] and i[self.china_field] != 'error' or i[self.idc_field] != 'error':

                sql = "UPDATE {} SET {} = %s WHERE {} = %s".format(self.table, self.result_name, i[0])

                val = (0, i[0])

                self.loggingFile(log_debug="{}".format("#####" * 20))

                self.loggingFile(log_debug="MySQL Output Equal", log_info=i)

                self.loggingFile(log_debug="{}".format("-----" * 20))

                self.loggingFile(log_debug="MySQL Output Equal info", log_info="id={}, idc={}, china={}".format(i[0], i[self.dns_field], i[self.china_field]))

                mycursor.execute(sql, val)

            self.mydb.commit()

            mycursor.execute("SELECT {} FROM {}".format(self.column, self.table))

            self.loggingFile(log_debug="{}".format("+++++" * 20))

            self.loggingFile(log_debug="MySQL Output Error info", log_info="{}".format(mycursor.fetchall()))



        return "Database UPDATE"







    def mysqlZabbixQuery(self):

        rVal = {

            "data" : []

        }

        dbdata = self.mysqlQuery()

        for i in dbdata:

            if int(i[self.result_field]) > 0:

                rVal["data"].append({

                    "{#DOMAIN}": i[self.domain_field],

                    "{#IDC}": i[self.idc_field],

                    "{#CHINA}": i[self.china_field],

                    "{#RESULT}": int(i[self.result_field])

                }



                )

        return json.dumps(rVal, indent=4)





















if __name__ == '__main__':

    print(DomainDNS().mysqlZabbixQuery())






