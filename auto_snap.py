#!/usr/bin/python3

import os
import sys
import threading
import logging
import time
import signal
from datetime import datetime

try:
    import queue
except ImportError:
    import Queue as queue

from autosnap.common.config import Config
from autosnap.flusher import Flusher
from autosnap.csvoper import CSVOper
from autosnap.cephoper.ceph_snapshot_op import CephSnaper
from autosnap.httpserver.snapshot_http_server import SnapshotHttpServer, SnapshotHttpServerHandler

snapshot_http_server = None
#CONF_FILE = os.path.abspath(os.getcwd()) + '/autosnap.conf'
CONF_FILE = '/etc/autosnap/autosnap.conf'

_LOG = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-8s %(message)s')
file_handler = logging.FileHandler("/var/log/autosnap.log")
file_handler.setFormatter(formatter)
_LOG.addHandler(file_handler)
_LOG.setLevel(logging.INFO)

def stop_service(signum, frame):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print("The autosnap service is stoped at {}".format(current_time))
    global snapshot_http_server
    snapshot_http_server.shutdown()
    sys.exit(0)

def main():
    # read start mode from command line
    # -r means restart the service
    # -n means start a new service
    start_mode = '-n'
    if len(sys.argv) >= 2:
        start_mode = sys.argv[1]
    _LOG.info('Start autosnap with the mode: {}'.format(start_mode))
    if start_mode == '-n':
        if not CSVOper.create():
            sys.exit(-1)

    Config.Parse(CONF_FILE)
    global snapshot_http_server
    snapshot_http_server = SnapshotHttpServer((Config.ip, Config.port), SnapshotHttpServerHandler)
    server_thread = threading.Thread(target = snapshot_http_server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    _LOG.info('Start Snapshot HTTPServer')

    signal.signal(signal.SIGINT, stop_service)

    flush_start_time = datetime.utcnow()
    snap_start_time = datetime.utcnow()
    flush_thread_running = False
    snapshot_thread_running = False
    while True:
        now = datetime.utcnow()
        flush_time_interval = (now - flush_start_time).seconds
        if flush_time_interval >= Config.flush_queue_interval:
            flush_thread = Flusher()
            flush_thread.start()
            flush_thread_running = True
            flush_start_time = now

        snapshot_time_interval = (now - snap_start_time).seconds
        if (Config.debug_interval != -1 and snapshot_time_interval >= Config.debug_interval) or \
           now.minute == 0 or snapshot_time_interval >= 3600:
            snapshot_thread = CephSnaper()
            snapshot_thread.start()
            snapshot_thread_running = True
            snap_start_time = now

        if flush_thread_running:
            flush_thread.join()
            flush_thread_running = False

        if snapshot_thread_running:
            snapshot_thread.join()
            snapshot_thread_running = False

        time.sleep(5)

if __name__ == '__main__':
    main()
