import threading
from datetime import datetime
from csvoper import CSVOper
from common.config import Config
from common.cli_op import CliOp

SNAP_CMD = {
    'create': 'rbd snap create {pool_name}/{image_name}@{snap_name}',
}

class CephSnaper(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        need_snapshot_images = CSVOper.read()
        now = datetime.utcnow()
        for image in need_snapshot_images:
            last = now
            print (image)
            if Config.debug_interval != -1:
                snapshot_period = int(image['snapshot_period']) * Config.debug_interval
            else:
                snapshot_period = int(image['snapshot_period']) * 3600

            if image['last_snapshot'] != '-':
                last_snapshot = image['last_snapshot']
                last = datetime.strptime(last_snapshot, '%Y-%m-%d %H:%M')
            # if now - last < snapshot_period; we need not snapshot the image in this clock
            if image['last_snapshot'] == '-' or (now - last).seconds >= snapshot_period:
                snap_name = Config.snapshot_prefix + now.strftime('%Y-%m-%d-%H:%M')
                args = SNAP_CMD['create'].format(pool_name = image['pool_name'], \
                                                 image_name = image['image_name'], \
                                                 snap_name = snap_name)
                CliOp.cli_op(args.split(' '))
                image['last_snapshot'] = now.strftime('%Y-%m-%d %H:%M')
                CSVOper.updaterow(image)
