import numpy as np
import cv2
from PIL import Image
from six import StringIO
import requests
import time

cap = cv2.VideoCapture(0)

last_sent = time.time()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    cv2.rectangle(frame,(384,0),(510,128),(0,255,0),3)


    if ((time.time() - last_sent) > 2):
        cv2.imwrite('image.jpg', frame)
        url = "http://146.169.3.104:5000/api"
        files = {'my_image': open('image.jpg', 'rb')}
        response = requests.post(url, files=files)
        print(response.text)
        last_sent = time.time()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
