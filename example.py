import rpicam_stream
import cv2

rpicam = rpicam_stream.Rpicam('192.168.0.7',8000)
while(1):
    image = rpicam.read()
    while(not rpicam.correct):
        image = rpicam.read()
    cv2.imwrite('./image/frame'+str(rpicam.save_idx())+'.jpg', image)

