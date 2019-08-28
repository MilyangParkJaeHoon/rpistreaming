import rpicam_stream
import cv2
import sys

tcp_ip = sys.argv[1]
tcp_port = int(sys.argv[2])

rpicam = rpicam_stream.Rpicam(tcp_ip, tcp_port)

while(1):
    image = rpicam.read()
    while(not rpicam.correct):
        image = rpicam.read()
    cv2.imwrite('./image/frame'+str(rpicam.save_idx())+'.jpg', image)

