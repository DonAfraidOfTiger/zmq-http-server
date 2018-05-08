# coding=utf-8
import time
import zmq
from zmq import devices



context = zmq.Context()
def worker():
    socket = context.socket(zmq.STREAM)
    socket.bind('tcp://*:5558')
    cnt=0
    while True:
        #  Wait for next request from client
        print(1)
        while True:
            message = socket.recv_multipart(copy=True)
            #print(2)
            #print("Received request: %s" % message)
            if len(message[1])>0:
                print(message[1].decode())
                break

        #socket.send_multipart([message[0],b'hello world'])
        cnt+=1
        http_response ="HTTP/1.0 200 OK\r\n"+ \
        "Content-Type: text/plain\r\n"+ \
        "Content-Length: 14\r\n"+ \
        "\r\n"+ \
        "Hello,World!%s\r\n" %cnt
        print(4)
        socket.send_multipart((message[0],http_response.encode()),flags=zmq.SNDMORE)
        #socket.send_multipart((message[0],b''), flags=zmq.SNDMORE)


worker()