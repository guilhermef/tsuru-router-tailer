import re
import socket
import tailer
import json

UDP_IP = "10.0.3.163"
UDP_PORT = 1984
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for message in tailer.follow(open('some.log')):
    tsuru_app = message.split(" ")[-3].replace('"', '').split('.')[0]
    value = message.split(" ")[-2]
    r = r'.* "(?P<method>\w+) (?P<path>.*) HTTP.*" (?P<status_code>\d{3}).*'
    info = re.search(r, message)

    dimensions = {
        "metric": "response_time",
        "client": "tsuru",
        "app": tsuru_app,
        "value": float(value),
        "path": info.groupdict()['path'],
        "method": info.groupdict()['method'],
        "status_code": info.groupdict()['status_code']
    }

    message = json.dumps(dimensions, separators=(',', ':'))
    print("message:", message)
    SOCK.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))
