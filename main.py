import json
from multiprocessing import Process

import asyncio
import socketio

from wmps.netperf import IperfClient
from wmps.ookla import speedtest
sio = socketio.AsyncClient()


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
#    await sio.sleep(1)
#    await sio.emit('start_speedtest')
#
@sio.event
async def disconnect():
    print('disconnected from server')

@sio.event
async def server_event(data):
    print(data)

async def main():
    await sio.connect('http://localhost:5000')
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())
