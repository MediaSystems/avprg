import numpy as np
import cv2

cap = cv2.VideoCapture('Micro-dance_2_.avi')

hueLowerThreshold = 170
hueUpperThreshold = 180
saturationThreshold = 120

while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break

    # Umwandlung in HSV-Farbraum mit cvtColor()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Aufspaltung in drei Graustufen-Bilder für H, S, V
    h, s, v = cv2.split(hsvFrame)

    # Segmentierung: threshold(), inRange()
    # Hue: 170 < hue < 180
    # Saturation: 120 < saturation
    hmask = cv2.inRange(h, hueLowerThreshold, hueUpperThreshold)
    #cv2.imshow("Hue Maske", hmask)
    
    ret, smask = cv2.threshold(s, saturationThreshold, 255, 
        cv2.THRESH_BINARY)
    #cv2.imshow("Saturation Maske", smask)    
    
    # Verknüpfung der beiden Masken (Hue, Saturation)
    mask = cv2.bitwise_and(hmask, smask)
    cv2.imshow("Maske", mask)
    
    # Schwerpunkt der weissen Pixel 
    M = cv2.moments(mask)
    if M["m00"]:
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        cv2.circle(frame, (cx, cy), 5, (0,0,255), cv2.FILLED)

    cv2.imshow("Video", frame)
    if cv2.waitKey(30) != -1:
        break
cap.release()
cv2.destroyAllWindows()