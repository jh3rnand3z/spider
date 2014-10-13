import time
import arrow
import motor

import logging

from tornado import gen
from tornado import web

from spider.system import inbound
from spider.messages import inbound as models
from spider.tools import errors

from spider.handlers import BaseHandler


class Handler(BaseHandler, inbound.Inbound):
    '''
        Inbound resource handler
    '''

    @gen.coroutine
    def get(self):
        pass

    @gen.coroutine
    def post(self):

        channel = 'SIP/gocella_18777786075/'
        
        callerid = '18777786075'
        context = 'DID_18777786075'
        extension = '18777786075'
        priority = 1

        max_retries = 2
        retry_time = 300
        wait_time = 45

        print self.request.arguments

        query_args = self.request.arguments
        
        try:
            phone_number = query_args.get('Phone1')[0]
        except IndexError:
            # raise missing phone error
            pass

        try:
            inbound_id = query_args.get('AccountID')[0]
        except IndexError:
            # raise missing inbound id
            pass

        first_name = query_args.get('firstName')[0]
        last_name = query_args.get('lastName')[0]


        dial_number = ''.join((channel, '1', phone_number))


        struct = {
            'account': inbound_id,
            'channel': dial_number,
            'callerid': callerid,
            'max_retries': max_retries,
            'retry_time': retry_time,
            'wait_time': wait_time,
            'context': context,
            'extension': extension,
            'priority': priority
        }

        try:
            call_file = models.Call(struct)
            call_file.validate()

            struct = call_file.to_primitive()
        except Exception, e:
            print 'error: ', e


        call_file = yield self.spawn_call_file(struct)

        dial = yield self.move_tmp_file(call_file)

        print dial
