import json
from multiprocessing import Process
from datetime import datetime
from time import time as timer
import asyncio
import socketio

from wmps.netperf import IperfClient
from wmps.ookla import speedtest
sio = socketio.AsyncClient()

last = 0
send_ping_to_server = True
async def send():
    global last
    last = timer()
    await sio.emit('ping_from_client')

async def background_task():
    proc = speedtest.run()
    while True:
        out = proc.stdout.readline()
        if out == '' and proc.poll() is not None:
            break
        if out:
            serialize = json.loads(out)
            await sio.sleep(0.1)
            await sio.emit('my response', serialize)

@sio.event
async def speedtest_task(data):
    print(data)
    await background_task()

@sio.event
async def connect():
    print('connection established')
    await sio.sleep(1)
    await send()
#    await sio.emit('start_speedtest')
#
@sio.event
async def disconnect():
    print('disconnected from server')

@sio.event
async def server_event(data):
    print(data)

@sio.event
async def stop_ping_server():
    global send_ping_to_server
    send_ping_to_server = False

@sio.event
async def pong_from_server():
    global last
    global send_ping_to_server
    latency = timer() - last
    last = latency
    await sio.emit('client_latency', {'data': latency})
    await sio.sleep(0.1)
    if send_ping_to_server:
        await send()

async def main():
    await sio.connect('http://localhost:5000')
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())
