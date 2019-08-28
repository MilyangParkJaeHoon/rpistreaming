import io
import socket
import struct
from PIL import Image
import cv2
import numpy
import time

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
# server_socket = socket.socket()
# server_socket.bind(('192.168.10.123', 8000))
# server_socket.listen(0)
client_socket =  socket.socket()
client_socket.connect(('192.168.10.123', 8000))
connection = client_socket.makefile('rb')
# Accept a single connection and make a file-like object out of it
# connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        start_time = time.time()
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        opencvImage = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        cv2.imshow('image',opencvImage)
        key = cv2.waitKey(1)
        if key == 27:
            break
        print('time : ', time.time()-start_time)
        # print('Image is %dx%d' % image.size)
        # image.verify()
        # print('Image is verified')
finally:
    connection.close()
    client_socket.close()