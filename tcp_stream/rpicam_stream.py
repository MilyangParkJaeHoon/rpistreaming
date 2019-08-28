import io
import socket
import struct
import time
from PIL import Image

class Rpicam(object):
    def __init__(self, tcp_ip, tcp_port):
        self.client_socket = socket.socket()
        self.client_socket.connect((tcp_ip, int(tcp_port)))
        self.connection = self.client_socket.makefile('rb')
        self.status = False

    def read(self):
        #send_time = struct.unpack('<d', self.connection.read(struct.calcsize('<d')))[0]
        # print('transport time : ',time.time() - send_time)
        image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            self.status = False
            return 0, 0
        else:
            self.status = True
        image_stream = io.BytesIO()
        image_stream.write(self.connection.read(image_len))
        image_stream.seek(0)
        image = Image.open(image_stream)
        return image
