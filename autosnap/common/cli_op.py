import sys
import logging
import json
import subprocess

_LOG = logging.getLogger(__name__)

class CliOp(object):
    @classmethod
    def cli_op(cls, args):
        _LOG.debug('<cli_op>: %s', ' '.join(args))
        rc = None
        if sys.version_info >= (3, 0):
            rc = subprocess.run(args, stdout=subprocess.PIPE, \
                                stderr=subprocess.PIPE, encoding='utf-8')
        else:
            rc = subprocess.Popen(args, stdout=subprocess.PIPE, \
                                  stderr=subprocess.PIPE)
            rc.wait()

        if not rc.returncode:
            if sys.version_info >= (3, 0):
                if rc.stderr and not rc.stdout:
                    result = rc.stderr.strip()
                else:
                    result = rc.stdout.strip()
            else:
                stdout = rc.stdout.read()
                stderr = rc.stderr.read()
                if stderr and not stdout:
                    result = stderr.strip()
                else:
                    result = stdout.strip()

            try:
                return json.loads(result)
            except ValueError:
                if not result:
                    _LOG.debug('<cli_op>: %s --> successfully', ' '.join(args))
                    result = 'success'
        else:
            _LOG.debug('<cli_op>: %s --> failed, return_code = %d, return_msg = %s' \
                       % (' '.join(args), rc.returncode, rc.stderr.strip()))
            result = 'failed'

        return {'result': result}
