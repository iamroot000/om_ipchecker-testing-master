import json
import mysql.connector


class SslMonitor():
   def toQueryDom(self):
      mydb = mysql.connector.connect(
          host="10.167.11.205",
          user="yrollrei",
          passwd="s22-C350",
          database="argus_v2"
      )

      mycursor = mydb.cursor()

      mycursor.execute("SELECT domain FROM domain_sslchecker WHERE daysleft<10")
      b = mycursor.fetchall()
      d = {"data":[]}
      for new_b in b:
        d["data"].append({"{#DOMAINSSL}":new_b[0]})
      return json.dumps(d)


if __name__=="__main__":
   a = SslMonitor()
   print(a.toQueryDom())

