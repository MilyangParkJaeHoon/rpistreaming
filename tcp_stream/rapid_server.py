import io
import socket
import struct
import time
import picamera
import sys

tcp_ip = sys.argv[1]
tcp_port = int(sys.argv[2])
cam_resolution = sys.argv[3]

class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            #now_time = time.time()
            if size > 0:
                #self.connection.write(struct.pack('<d', now_time))
                #self.connection.flush()
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)

server_socket = socket.socket()
server_socket.bind((tcp_ip, tcp_port))
server_socket.listen(0)
print('Wait client.................')
connection = server_socket.accept()[0].makefile('wb')
print('Connected!!!')
try:
    output = SplitFrames(connection)
    with picamera.PiCamera(resolution=cam_resolution, framerate=15) as camera:
        time.sleep(2)
        start = time.time()
        camera.start_recording(output, format='mjpeg')
        #camera.wait_recording(10)
        while True:
            pass
        camera.stop_recording()
        # Write the terminating 0-length to the connection to let the
        # server know we're done
        connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    server_socket.close()
    finish = time.time()
print('Sent %d images in %d seconds at %.2ffps' % (
    output.count, finish-start, output.count / (finish-start)))
