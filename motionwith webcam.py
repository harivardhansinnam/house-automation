import threading
import winsound
import playsound
import cv2
import datetime

"""background = cv2.imread("123.jpg")
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
background = cv2.GaussianBlur(background, (21, 21), 0)"""

video = cv2.VideoCapture(0)
first_frame=None
alarm = False
alarm_mode = False
alarm_counter = 0
now = datetime.datetime.now()
curtime = int(now.strftime("%H"))
def alert():
    global alarm

    if alarm_mode:

      winsound.Beep(2500,250)
      alarm=False

if (curtime) > 23 or (curtime) < 6:
    alarm_mode = True

while True:
    if alarm_mode:

        status, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if first_frame is None:
            first_frame=gray
            continue
        diff = cv2.absdiff(first_frame, gray)

        thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        if thresh.sum()>300:
            alarm_counter+=1
        else:
            if alarm_counter>0:
                alarm_counter-=1
        cnts,res = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
                if cv2.contourArea(contour) < 10000 :
                        continue
                (x,y,w,h) = cv2.boundingRect(contour)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0), 3)

        cv2.imshow("All Contours",frame)


        if alarm_counter>15:
            if not alarm:
                alarm=True
                threading.Thread(target=alert).start()

        key=cv2.waitKey(1)
        if key == ord("q"):
            alarm_counter=0
            alarm=False
            break

video.release()
cv2.destroyAllWindows()