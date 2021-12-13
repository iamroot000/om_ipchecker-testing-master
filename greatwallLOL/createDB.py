import mysql.connector

mydb = mysql.connector.connect(
  host="10.165.22.205",
  user="yrollrei",
  passwd="s22-C350",
  database="argus_v2"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE dnschina_checker (id INT AUTO_INCREMENT PRIMARY KEY, domain VARCHAR(255), dns VARCHAR(50), china VARCHAR(50), result VARCHAR(50))")
#mycursor.execute("CREATE TABLE dnsdomainchecker (id INT AUTO_INCREMENT PRIMARY KEY, domain VARCHAR(255), idc VARCHAR(50), registrar VARCHAR(50), china VARCHAR(50), dns VARCHAR(50), date VARCHAR(50), result VARCHAR(50))")
mycursor.execute("CREATE TABLE dnsdomainchecker (id INT AUTO_INCREMENT PRIMARY KEY, domain VARCHAR(255), idc VARCHAR(50), registrar TEXT, china VARCHAR(50), dns VARCHAR(50), date VARCHAR(50), result VARCHAR(50))")

