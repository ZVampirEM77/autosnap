#!/usr/bin/python3

import sys

if sys.version_info >= (3, 0):
    from socketserver import ThreadingMixIn
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    from SocketServer import ThreadingMixIn

from common.shop_queue import ShopQueue


class SnapshotHttpServer(ThreadingMixIn, HTTPServer):
    pass


class SnapshotHttpServerHandler(BaseHTTPRequestHandler):

    protocol_version = 'HTTP/1.1'
    # for debug
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("SnapshotHttpServerHandler::do_POST\n".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        ShopQueue.shop_queue.put(post_data)
        self.send_response(200)
        self.send_header('Content-Length', '0')
        self.end_headers()
