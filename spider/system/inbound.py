import motor
import uuid # ?

from shutil import move

from tornado import gen

from howler.messages import outbound
from howler.tools.call import CallFile


# growls? "howls"??

class Outbound(object):
    '''
        Outbound call resources
    '''

    @gen.coroutine
    def move_tmp_file(self, tmp_file):
        '''
            move tmp .call file to outgoing directory
        '''
        try:
            move(tmp_file, self.spool_dir)
        except Exception, e:
            # return error if any.

            # Python 2.7.X only.
            # Special exception to return a value from a coroutine.

            # In Python >= 3.3, this exception is no longer necessary: 
            # the return statement can be used directly to return a value

            raise gen.Return(e)

    @gen.coroutine
    def spawn_call_file(self, struct):
        '''
            spawn asterisk .call file
        '''
        cfile = CallFile()
        call_path = cfile.generate_call(self.tmp_dir,
            struct.get('channel'),
            struct.get('callerid'),
            struct.get('max_retries'),
            struct.get('retry_time'),
            struct.get('wait_time'),
            struct.get('context'),
            struct.get('extension'),
            struct.get('priority')
        )

        # Python 2.7.X only.
        # Special exception to return a value from a coroutine.

        # In Python >= 3.3, this exception is no longer necessary: 
        # the return statement can be used directly to return a value

        raise gen.Return(call_path)

    @gen.coroutine
    def check_outgoing_files(self):
        '''
            check concurrent outgoing calls
        '''
        pass