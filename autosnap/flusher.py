import threading
import time
import datetime
import logging
from autosnap.csvoper import CSVOper
from autosnap.common.shop_queue import ShopQueue

_LOG = logging.getLogger('__main__.' + __name__)

class Flusher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not ShopQueue.shop_queue.empty():
            # bytes --> string --> dict
            ele = eval(str(ShopQueue.shop_queue.get(), encoding = 'utf-8'))
            req_type = ele.pop('type')
            _LOG.info('Get queue {} {}, request type is {}'.format(type(ele), ele, req_type))
            if req_type == 'add':
                ele['last_snapshot'] = '-'
                if not CSVOper.writerow(ele):
                    _LOG.error('Add csv entry failed!')
                    pass
            elif req_type == 'update':
                ele['last_snapshot'] = '-'
                if not CSVOper.updaterow(ele):
                    _LOG.error('Update csv entry failed!')
                    pass
            elif req_type == 'delete':
                if not CSVOper.deleterow(ele):
                    _LOG.error('Delete csv entry failed')
                    pass

            time.sleep(5)
