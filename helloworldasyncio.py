# coding=utf-8
import zmq
from zmq.asyncio import Context, Poller
import asyncio
import zlib
import  pickle



context = zmq.asyncio.Context()
socket = context.socket(zmq.STREAM)
socket.bind('tcp://*:5555')
cnt=0
async def worker(name):


    while True:
        #  Wait for next request from client
        #print(1)
        while True:
            message =await socket.recv_multipart(copy=True)
            #print(2)
            #print("Received request: %s" % message)
            if len(message[1])>0:
                #print(name,message[1].decode())
                break
        if False:
            #socket.send_multipart([message[0],b'hello world'])
            global cnt
            cnt+=1
            body="Hello,World!,%03d,%012d\r\n" %(name,cnt)
            header="HTTP/1.0 200 OK\r\n"+ \
            "Content-Type: text/plain\r\n"+ \
            "Content-Length: %s\r\n"  %len(body.encode())
            http_response=header+"\r\n" + body
            await socket.send_multipart((message[0], http_response.encode()), flags=zmq.SNDMORE)
        else:
            http_response=b'HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 13\r\n\r\nhello worlf\r\n'
            await socket.send_multipart((message[0], http_response), flags=zmq.SNDMORE)
            await socket.send_multipart((message[0], b''), flags=zmq.SNDMORE)

        #await socket.send_multipart((message[0],b''), flags=zmq.SNDMORE)



asyncio.get_event_loop().run_until_complete(asyncio.wait([

    worker(i) for i in range(120)
    #sender(),
]))
