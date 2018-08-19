import threading
import time
import datetime
from autosnap.csvoper import CSVOper
from autosnap.common.shop_queue import ShopQueue

class Flusher(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while not ShopQueue.shop_queue.empty():
            # bytes --> string --> dict
            ele = eval(str(ShopQueue.shop_queue.get(), encoding = 'utf-8'))
            print ("in flusher get queue {} {}".format(type(ele), ele))
            req_type = ele.pop('type')
            if req_type == 'add':
                ele['last_snapshot'] = '-'
                if not CSVOper.writerow(ele):
                    #logging
                    pass
            elif req_type == 'update':
                ele['last_snapshot'] = '-'
                if not CSVOper.updaterow(ele):
                    print ("csv update failed")
                    #logging
                    pass
            elif req_type == 'delete':
                if not CSVOper.deleterow(ele):
                    print ("csv delete failed")
                    #logging
                    pass

            time.sleep(5)
