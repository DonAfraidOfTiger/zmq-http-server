# coding=utf-8
import zlib
import pickle

import numpy

import zmq
from temp.serialsocket import SerializingSocket,SerializingContext
def main():
    ctx = SerializingContext()
    #req = ctx.socket(zmq.REQ)
    rep = ctx.socket(zmq.REP)

    #req.bind('tcp://127.0.0.1:1234')
    rep.connect('tcp://104.216.151.131:8080')
    cnt=0
    while True:
        A = numpy.ones((1024, 50))
        print("Array is %i bytes" % (A.nbytes))
        B = rep.recv_zipped_pickle()
        cnt+=1
        rep.send_array(A, copy=False)
        print(cnt)




if __name__ == '__main__':
    main()