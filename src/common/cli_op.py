import logging
import json
import subprocess

_LOG = logging.getLogger(__name__)

class CliOp(object):
    @classmethod
    def cli_op(cls, args):
        _LOG.debug('<cli_op>: %s', ' '.join(args))
        rc = subprocess.run(args, stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE, encoding='utf-8')

        if not rc.returncode:
            if rc.stderr and not rc.stdout:
                result = rc.stderr.strip()
            else:
                result = rc.stdout.strip()

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
