import json
import re
from multiprocessing import Process
from datetime import datetime
from time import time as timer
import asyncio
import socketio

from wmps.netperf import IperfClient
from wmps import ping
from wmps.ookla import speedtest

sio = socketio.AsyncClient()

last = 0
send_ping_to_server = True

async def send():
    global last
    last = timer()
    await sio.emit('ping_from_client')

async def background_task(msg):
    task = msg.get('task')
    if task == 1:
        proc = speedtest.run()
        while task:
            out = proc.stdout.readline()
            if out == '' and proc.poll() is not None:
                break
            if out:
                serialize = json.loads(out)
                await sio.sleep(0.1)
                await sio.emit('my response', serialize)
                
    elif task == 2:
        addr = msg.get('data')
        proc = ping.run(addr)
        print(proc)
        while task:
            out = proc.stdout.readline()
            match = re.search("time=\d+.\d+", out)
            if not match == None:
                match = match.group(0)
                rtt = match.split("=")[1]
                await sio.sleep(0.1)
                await sio.emit('ping_event', {'data': rtt})
    elif task == 3:
        config = msg.get('data')
        server = config.get('server')
        reverse = config.get(int('reverse'))
        client = IperfClient(server_hostname=server, reverse=reverse, json_output=True, serveroutput=True)
        proc = iperf3.run(server)

@sio.event
async def run_task(msg):
    print(msg)
    # we run one task at a time
    await background_task(msg)

@sio.event
async def connect():
    print('connection established')
    await sio.sleep(1)
    await sio.emit('join_dashboard')
    await send()
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
