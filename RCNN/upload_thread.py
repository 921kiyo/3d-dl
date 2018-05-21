import numpy as np
import cv2
from PIL import Image
from six import StringIO
import requests
import time
import threading
import json

cap = cv2.VideoCapture(0)

last_sent = time.time()

my_threads = []

thread_counter = 0

ret, frame = cap.read()
current_frame = frame
current_rectangles = []
current_classes = []

labels_to_names = {0:'Anchor', 1:'Coconut', 2:'CottageCheese', 3:'Halloumi', 4:'Liberte', 5:'MangoYogurt', 6:'Soup', 7:'SoyMilk', 8:'Squashums', 9:'StrawberryYogurt'}

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      cv2.imwrite('image1.jpg', current_frame)
      url = "http://146.169.3.104:5000/detector"
      files = {'my_image': open('image1.jpg', 'rb')}
      response = requests.post(url, files=files)
      print(response.text)
      results = json.loads(response.text)
      # current_rectangles = []
      current_rectangles.clear()
      current_classes.clear()
      for result in results:
          scaling_constant = 720/224
          rmin = int(float(result[1])*scaling_constant)
          cmin = int(float(result[2])*scaling_constant)
          rmax = int(float(result[3])*scaling_constant)
          cmax = int(float(result[4])*scaling_constant)
          rectangle = [rmin, cmin, rmax, cmax]
          current_rectangles.append(rectangle)

          b_row = rmin
          b_col = cmin - 25
          current_class = labels_to_names[int(result[0])]
          class_classification = [current_class, b_row, b_col]
          current_classes.append(class_classification)

      # self.exit()




while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    current_frame = frame
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    if ((time.time() - last_sent) > 0.2):
        my_threads.append(myThread(thread_counter, str(thread_counter), thread_counter))
        my_threads[thread_counter].start()
        last_sent = time.time()
        thread_counter += 1
    # Display the resulting frame
    crop_img = frame[0:720, 280:1000]

    for rectangle in current_rectangles:
        cv2.rectangle(crop_img ,(rectangle[0],rectangle[1]),(rectangle[2],rectangle[3]),(0,255,0),3)

    for current_class in current_classes:
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(crop_img,current_class[0],(current_class[1],current_class[2]), font, 1.5,(255,255,255),2,cv2.LINE_AA)

    cv2.imshow("cropped", crop_img)
    # cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):

        break


for t in my_threads:
   t.join()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
