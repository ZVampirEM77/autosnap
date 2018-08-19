import sys

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
    def Parse(cls, config_file = '../../autosnap.conf'):
        autosnap_conf = ConfigParser()
        autosnap_conf.read(config_file)
        Config.ip = autosnap_conf.get('global', 'ip')
        Config.port = autosnap_conf.getint('global', 'port')
        Config.debug_interval = autosnap_conf.getint('global', 'debug_interval')
        Config.flush_queue_interval = autosnap_conf.getint('global', 'flush_queue_interval')
        Config.snapshot_prefix = autosnap_conf.get('global', 'snapshot_prefix')
