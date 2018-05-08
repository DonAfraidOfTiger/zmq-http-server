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
from datetime import datetime,timedelta

dev = devices.ThreadDevice(device_type=zmq.QUEUE,
                               in_type=zmq.ROUTER,out_type=zmq.DEALER)

dev.bind_in('tcp://127.0.0.1:8096')
dev.bind_out('tcp://*:8092')
dev.start()

#wait for connections
time.sleep(1)
url = 'tcp://127.0.0.1:8096'

ctx = Context.instance()


def send_zipped_pickle( obj, flags=0, protocol=-1):
    pobj = pickle.dumps(obj, protocol)
    zobj = zlib.compress(pobj)
    #print('zipped pickle is %i bytes' % len(zobj))
    return zobj


def recv_zipped_pickle(zobj):

    pobj = zlib.decompress(zobj)
    return pickle.loads(pobj)



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
        req = ctx.socket(zmq.CLIENT)
        req.connect(url)
        poller = Poller()
        poller.register(req, zmq.POLLIN)
        return req,poller
    req,poller=reinitreq()
    while True:
        cnt+=1

        #await asyncio.sleep(1)
        print("send",cnt)
        t1=datetime.utcnow()
        at1=t1 - t0
        t0=t1
        print('dealy:%f' %at1.total_seconds())
        req.send(send_zipped_pickle([name,cnt,err,at1.total_seconds()]))
        events = await poller.poll(timeout=1000*10)
        if req in dict(events):
            resp=req.recv()
            print("resp:",recv_zipped_pickle(resp))
        else:
            err += 1
            print('failed',err)
            req,poller=reinitreq()

        #await asyncio.sleep(1)
    print('exit r')

asyncio.get_event_loop().run_until_complete(asyncio.wait([
    sender(i) for i in range(60)
]))
