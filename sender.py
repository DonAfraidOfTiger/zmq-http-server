"""Example using zmq with asyncio coroutines"""
# Copyright (c) PyZMQ Developers.
# This example is in the public domain (CC-0)
import sys
sys.path=['../toollib/',
            './',
          '../../'
          ]+sys.path
import time

import zmq
from zmq.asyncio import Context, Poller
import asyncio

import sys
import zmq
from zmq import devices
import zlib
import pickle
#import  cPickle as pickle
from datetime import datetime,timedelta
import blosc
import marshal

dev = devices.ThreadDevice(device_type=zmq.QUEUE,
                               in_type=zmq.ROUTER,out_type=zmq.DEALER)

dev.bind_in('tcp://127.0.0.1:8086')
dev.bind_out('tcp://*:8082')
dev.start()

#wait for connections
time.sleep(1)
url = 'tcp://127.0.0.1:8086'

ctx = Context.instance()

def decompress(bobj):
    #pobj = zlib.decompress(bobj)
    pobj=blosc.decompress(bobj)
    #return pickle.loads(pobj)
    return marshal.loads(pobj)
def compress(obj):
    #pobj = pickle.dumps(obj, -1)
    pobj = marshal.dumps(obj, -1)

    #cobj = zlib.compress(pobj)
    cobj=blosc.compress(pobj,typesize=8)
    return cobj


async def sender(name=0):
    """send a message every second"""
    tic = time.time()

    cnt=0
    err=0
    print('start')
    t0=datetime.utcnow()
    def reinitreq(req=None):
        if req:
            req.close()
            del req
        req = ctx.socket(zmq.REQ)
        req.connect(url)
        poller = Poller()
        poller.register(req, zmq.POLLIN)
        return req,poller
    req,poller=reinitreq()
    import numpy
    while True:
        cnt+=1

        #await asyncio.sleep(1)
        print("send",cnt)
        t1=datetime.utcnow()
        at1=t1 - t0
        t0=t1
        print('dealy:%f' %at1.total_seconds())
        A = numpy.ones((1024, 1024))
        req.send(send_zipped_pickle([name,cnt,err,at1.total_seconds(),A]))
        events = await poller.poll(timeout=1000*10)
        if req in dict(events):
            resp=req.recv()
            print("resp:",recv_zipped_pickle(resp))
        else:
            err += 1
            print('failed',err)

            req,poller=reinitreq()

        #await asyncio.sleep(1)


asyncio.get_event_loop().run_until_complete(asyncio.wait([
    sender(i) for i in range(60)
]))
'''

firewall-cmd --permanent --zone=public --add-port=8082/tcp
systemctl restart firewalld
'''