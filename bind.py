# coding=utf-8
import zlib
import pickle

import numpy

import zmq
from temp.serialsocket import SerializingSocket,SerializingContext
def main():
    ctx = SerializingContext()
    req = ctx.socket(zmq.REQ)
    #rep = ctx.socket(zmq.REP)

    req.bind('tcp://127.0.0.1:1234')
    #rep.connect('tcp://127.0.0.1:1234')
    cnt=0
    while True:
        A = numpy.ones((1024, 1024))
        print("Array is %i bytes" % (A.nbytes))

        # send/recv with pickle+zip
        req.send_zipped_pickle(A)
        #B = rep.recv_zipped_pickle()
        # now try non-copying version
        #rep.send_array(A, copy=False)
        C = req.recv_array(copy=False)
        cnt += 1
        print(cnt)



if __name__ == '__main__':
    main()