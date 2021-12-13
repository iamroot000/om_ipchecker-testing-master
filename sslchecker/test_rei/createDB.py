import mysql.connector

mydb = mysql.connector.connect(
  #host="10.167.11.205",
  host="10.165.22.205",
  user="yrollrei",
  passwd="s22-C350",
  database="argus_v2"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE domain_sslcheckertest (id INT AUTO_INCREMENT PRIMARY KEY, domain VARCHAR(255), status VARCHAR(255), date_now VARCHAR(255), expiration VARCHAR(255), daysleft VARCHAR(255), port80 VARCHAR(255), port443 VARCHAR(255), skip VARCHAR(255), business_unit VARCHAR(255))")
print("Table created!")

