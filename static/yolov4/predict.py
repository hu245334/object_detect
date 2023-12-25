# -------------------------------------#
#       对单张图片进行预测
# -------------------------------------#
import glo
from yolo import YOLO
from PIL import Image
import pymysql

glo._init()
glo.set_value('count_person', 0)
glo.set_value('count_car', 0)

yolo = YOLO()

conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="imgdetect"
)

cur = conn.cursor()
result = cur.execute("select img from login_img order by date2 desc ")
result = cur.fetchall()

while True:
    url = ((result[0])[0])
    print(url)
    img = "static/media/" + ((result[0])[0])
    try:
        image = Image.open(img)
    except:
        print('Open Error! Try again!')
        continue
    else:
        r_image = yolo.detect_image(image)
        r_image.save('static/media/deimg/' + ((result[0])[0]))
        break
