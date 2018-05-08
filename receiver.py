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
import zlib
import  pickle

def send_zipped_pickle( obj, flags=0, protocol=-1):
    pobj = pickle.dumps(obj, protocol)
    zobj = zlib.compress(pobj)
    #print('zipped pickle is %i bytes' % len(zobj))
    return zobj


def recv_zipped_pickle(zobj):

    pobj = zlib.decompress(zobj)
    return pickle.loads(pobj)

urls = [
        #'tcp://104.216.151.131:8082',
        'tcp://199.180.102.17:8082']
#url = 'tcp://127.0.0.1:8082'
ctx = Context.instance()

import numpy


async def receiver(name=''):
    """receive messages with polling"""
    rep = ctx.socket(zmq.REP)
    for url in urls:
        rep.connect(url)
    poller = Poller()
    poller.register(rep, zmq.POLLIN)
    cnt=0
    while True:
        cnt+=1
        events = await poller.poll()
        if rep in dict(events):
            msg =await rep.recv()
            print(name,'recvd',recv_zipped_pickle(msg))
        print(name,'send:',cnt)
        A = numpy.ones((1024, 1024))
        rep.send(send_zipped_pickle([cnt,A]))






asyncio.get_event_loop().run_until_complete(asyncio.wait([

    receiver(i) for i in range(30)
    #sender(),
]))
