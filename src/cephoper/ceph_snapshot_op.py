import threading
from operator import itemgetter
from datetime import datetime
from csvoper import CSVOper
from common.config import Config
from common.cli_op import CliOp

SNAP_CMD = {
    'create': 'rbd snap create {pool_name}/{image_name}@{snap_name}',
    'delete': 'rbd snap rm {pool_name}/{image_name}@{snap_name}',
    'list': 'rbd snap list {pool_name}/{image_name} --format json'
}

class CephSnaper(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        need_snapshot_images = CSVOper.read()
        now = datetime.utcnow()
        for image in need_snapshot_images:
            if image['retain_count'] != '-' or image['retain_period'] != '-':
                list_args = SNAP_CMD['list'].format(pool_name = image['pool_name'],
                                                    image_name = image['image_name'])
                unordered_snap_list = CliOp.cli_op(list_args.split(' '))
                ordered_snap_list = sorted(unordered_snap_list, key=itemgetter('id'))
                if image['retain_count'] != '-':
                    if len(ordered_snap_list) >= int(image['retain_count']):
                        for i in range(len(ordered_snap_list) - int(image['retain_count']) + 1):
                            delete_args = SNAP_CMD['delete'].format(pool_name = image['pool_name'],
                                                                    image_name = image['image_name'],
                                                                    snap_name = ordered_snap_list[i]['name'])
                            CliOp.cli_op(delete_args.split(' '))
                        # TODO enming need add error processing

                elif image['retain_period'] != '-':
                    for snap in ordered_snap_list:
                        if Config.debug_interval != -1:
                            snap_create_time = datetime.utcfromtimestamp(datetime.strptime(snap['timestamp'], \
                                                    '%a %b %d %H:%M:%S %Y').timestamp())
                            if (now - snap_create_time).seconds > (int(image['retain_period']) * Config.debug_interval):
                                delete_args = SNAP_CMD['delete'].format(pool_name = image['pool_name'],
                                                                        image_name = image['image_name'],
                                                                        snap_name = snap['name'])
                                CliOp.cli_op(delete_args.split(' '))
                        else:
                            snap_create_date = datetime.strptime(datetime.strptime(snap['timestamp'], '%a %b %d %H:%M:%S %Y') \
                                                    .strftime('%Y-%m-%d'), '%Y-%m-%d')
                            today = datetime.strptime(now.strftime('%Y-%m-%d'), '%Y-%m-%d')
                            if (today - snap_create_date) > int(image['retain_period']):
                                delete_args = SNAP_CMD['delete'].format(pool_name = image['pool_name'],
                                                                        image_name = image['image_name'],
                                                                        snap_name = snap['name'])
                                CliOp.cli_op(delete_args.split(' '))
                        # TODO enming need add error processing

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
