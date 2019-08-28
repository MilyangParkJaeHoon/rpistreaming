import cv2
import numpy
import time
import rpicam_stream
import sys

tcp_ip = sys.argv[1]
tcp_port = int(sys.argv[2])
show_on = int(sys.argv[3])

start_time = time.time()
frame_count = 0
total_time = 0

rpicam = rpicam_stream.Rpicam(tcp_ip, tcp_port)

while True:
    send_time, frame = rpicam.read()

    if(rpicam.status == False):
        print('Can not read image')
        break
    
    frame_count += 1
    total_time += time.time() - send_time + 1

    if(show_on):
        opencvImage = cv2.cvtColor(numpy.array(frame), cv2.COLOR_RGB2BGR)
        cv2.imshow('image',opencvImage)
        key = cv2.waitKey(1)
        if key == 27:
            break

    time_gap = time.time()-start_time
    if(time_gap > 1):
        #print('avg transport time :\t',total_time/frame_count)
        print('fps :\t\t\t',frame_count/time_gap)
        print('--------------------\n')
        start_time = time.time()
        frame_count = 0
        total_time = 0

self.connection.close()
self.client_socket.close()
