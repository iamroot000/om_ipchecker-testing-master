import mysql.connector

mydb = mysql.connector.connect(
  #host="10.167.11.205",
  host="10.165.22.205",
  user="yrollrei",
  passwd="s22-C350",
  database="argus_v2"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE domain_sslchecker (id INT AUTO_INCREMENT PRIMARY KEY, domain VARCHAR(255), expiry VARCHAR(255), daysleft VARCHAR(255))")

