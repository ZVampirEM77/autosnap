#!/usr/bin/python3

import sys
import re

if sys.version_info >= (3, 0):
    from socketserver import ThreadingMixIn
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    from SocketServer import ThreadingMixIn

from csvoper import CSVOper
from common.shop_queue import ShopQueue


class SnapshotHttpServer(ThreadingMixIn, HTTPServer):
    pass


class SnapshotHttpServerHandler(BaseHTTPRequestHandler):

    protocol_version = 'HTTP/1.1'
    # for debug
    def do_GET(self):
        enabled = False
        if '/enable_query' in self.path:
            match_obj = re.match('/enable_query\/(.*)\/(.*)', self.path)
            req_pool = match_obj.group(1)
            req_image = match_obj.group(2)
            print("pool = {}, image = {}".format(req_pool, req_image))
            current_enable_images = CSVOper.read()
            for image in current_enable_images:
                if image['image_name'] == req_image and image['pool_name'] == req_pool:
                    enabled = True
        self.send_response(200)
        if enabled:
            self.send_header('Content-Length', '4')
            self.end_headers()
            self.wfile.write("True".encode('utf-8'))
        else:
            self.send_header('Content-Length', '5')
            self.end_headers()
            self.wfile.write("False".encode('utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        ShopQueue.shop_queue.put(post_data)
        self.send_response(200)
        self.send_header('Content-Length', '0')
        self.end_headers()
