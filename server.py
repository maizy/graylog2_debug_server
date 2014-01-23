#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
from __future__ import unicode_literals

import sys
import pprint

try:
    import SocketServer as socketserver
except ImportError:
    import socketserver

import gelf_decoder


class Graylog2TestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        ip = self.client_address[0]
        if data[0:2] == gelf_decoder.MAGIC:
            print('Chunk from {} with len={}'.format(ip, len(data)))
        else:
            print('Log entity from {}:'.format(ip))
            decoded = gelf_decoder.decode_full(data)
            print(pprint.pformat(decoded) if decoded is not None else '<Unable to decode>')


if __name__ == '__main__':
    host = b'0.0.0.0'
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 12201
    print('Listen UDP {0}:{1}'.format(host.decode('ascii'), port))
    server = socketserver.UDPServer((host, port), Graylog2TestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stoped. Bye!')
