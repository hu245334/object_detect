# -------------------------------------#
#       调用摄像头检测
# -------------------------------------#
import pymysql
import datetime
from yolo import YOLO
from PIL import Image
import numpy as np
import cv2
import time
import glo

glo._init()
glo.set_value('count_person', 0)
glo.set_value('count_car', 0)

conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="imgdetect"
)

yolo = YOLO()
# 调用摄像头
capture = cv2.VideoCapture(0)
# capture=cv2.VideoCapture("D:/TIMFile/MobileFile/video_20210127_144916_edit.mp4")

fps = 0.0
while (True):
    t1 = time.time()
    # 读取某一帧
    ref, frame = capture.read()
    # 格式转变，BGRtoRGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 转变成Image
    frame = Image.fromarray(np.uint8(frame))

    # 进行检测
    frame = np.array(yolo.detect_image(frame))

    # 数据写入数据库
    person = glo.get_value('count_person')
    car = glo.get_value('count_car')
    sql = "insert into login_datasource (id,source_date,person,car) values (\"" + str(time.time()) + "\",\"" + str(datetime.datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S')) + "\"," + str(person) + "," + str(car) + ")"
    print(sql)
    cur = conn.cursor()
    time.sleep(0.25)
    cur.execute(sql)
    conn.commit()
    cur.close()

    # RGBtoBGR满足opencv显示格式
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    fps = (fps + (1. / (time.time() - t1))) / 2
    print("fps= %.2f" % (fps))
    frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("video", frame)

    c = cv2.waitKey(1) & 0xff
    if c == 27:
        capture.release()
        break
