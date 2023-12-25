import pymysql

conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="ImgDetect"
)

cur = conn.cursor()
count = 82
cur.execute("select img from login_img where id = " + str(count))
