if sys.version_info >= (3, 0):
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser

class Config(object):
    ip = ''
    port = 0
    debug_interval = -1
    flush_queue_interval = 0

    @classmethod
    def Parse(cls, config_file = '../autosnap.conf'):
        autosnap_conf = ConfigParser()
        autosnap_conf.read('../' + config_file)
        ip = autosnap_conf.get('global', 'ip')
        port = autosnap_conf.getint('global', 'port')
        debug_interval = autosnap_conf.getint('global', 'debug_interval')
        flush_queue_interval = autosnap_conf.getint('global', 'flush_queue_interval')
