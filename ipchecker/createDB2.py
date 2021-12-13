import mysql.connector

mydb = mysql.connector.connect(
  host="10.167.11.205",
  user="yrollrei",
  passwd="s22-C350",
  database="argus_v2"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE gameapi_ipchecker (id INT AUTO_INCREMENT PRIMARY KEY, api VARCHAR(255), ip VARCHAR(255), result VARCHAR(255))")
