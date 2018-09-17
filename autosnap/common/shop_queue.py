try:
    import queue
except ImportError:
    import Queue as queue

class ShopQueue(object):
    shop_queue = queue.Queue()
