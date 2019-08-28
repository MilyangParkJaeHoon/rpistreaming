import cv2
import time

class Rpicam(object):
    def __init__(self, tcp_ip, tcp_port):
        self.video_url = "http://"+tcp_ip+":"+str(tcp_port)+"/stream.mjpg"
        self.capture_time = time.time()
        self.process_time = time.time()
        self.frame_time = time.time()
        self.frame_count = 0
        self.fps = 0
        self.idx = 0
        self.correct = False

    def reset_capture_time(self):
        self.capture_time = time.time()

    def reset_process_time(self):
        self.process_time = time.time()

    def reset_frame_time(self):
        self.frame_time = time.time()

    def reset_frame_count(self):
        self.frame_count = 0

    def print_capture_time(self):
        print(time.time() - self.capture_time)

    def print_process_time(self):
        print(time.time() - self.process_time)

    def save_idx(self):
        self.idx += 1
        return self.idx

    def fps_check(self):
        time_gap = time.time() - self.frame_time
        self.frame_count += 1
        if(time_gap >= 1):
            self.fps = round(self.frame_count/time_gap,2)
            self.reset_frame_count()
            self.reset_frame_time()

    def read(self):
        self.reset_capture_time()
        cap = cv2.VideoCapture(self.video_url)
        self.print_capture_time()

        self.reset_process_time()
        ret, frame = cap.read()
        if(hasattr(frame, 'size')):
            self.fps_check()
            cv2.putText(frame, str(self.fps), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 0, 0), 1)
            self.correct = True
        else:
            self.correct = False
            return 0
        
        self.print_process_time()
        
        return frame
        
        

