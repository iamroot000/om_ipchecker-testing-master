import mysql.connector
import socket


class greatChecker(object):


	def __init__(self,host,user,passwd,dbase):
		self.host=host
		self.user=user
		self.passwd=passwd
		self.dbase=dbase


	def conn(self):
		mydb = mysql.connector.connect(
			host=self.host,
			user=self.user,
			passwd=self.passwd,
			database=self.dbase
		)
		return mydb


	def get_dom(self):
		mydb = self.conn()
		cur = mydb.cursor()
		cur.execute("SELECT domain FROM dnschecker_dnschecker")
		domains = cur.fetchall()
		return domains

	def get_china_ip(self,dom):
		mydb = self.conn()
		cur = mydb.cursor()
		sql = "SELECT beijing FROM dnschecker_dnschecker WHERE domain = %s"
		tdom = (dom,)
		cur.execute(sql,tdom)
		ip = cur.fetchone()
		return ip

	def get_dns_ip(self,dom):
		try:
			ip = socket.gethostbyname(dom)
		except Exception as e:
			print('owshit!')
			print(e)
			return 'none'
		return str(ip)

	def lezdodiz(self):
		lizt = self.get_dom()
		mydb = self.conn()
		cur = mydb.cursor()
		for dom in lizt:
			(dom,) = dom
			dom = str(dom)
			china_ip = self.get_china_ip(dom)
			(china_ip,) = china_ip
			dns_ip = self.get_dns_ip(dom)
			china_ip = str(china_ip)
			sql = "INSERT INTO dnschina_checker(domain,dns,china,result) VALUES(%s,%s,%s,%s)"
			if dns_ip == china_ip:
				res = '1'
			else:
				res = '0'

			val = (dom,dns_ip,china_ip,res)
			
			cur.execute(sql,val)
			print val
		mydb.commit()
		return True




if __name__=="__main__":
	host = "10.165.22.205"
	user = "yrollrei"
	passwd = "s22-C350"
	dbase = "argus_v2"

	g = greatChecker(host,user,passwd,dbase)	

	g.lezdodiz()


