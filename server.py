import os
import logging
import motor

from tornado import ioloop
from tornado import gen
from tornado import web

from howler.handlers import outbound

from howler.tools import options
from howler.tools import indexes


class IndexHandler(web.RequestHandler):
    '''
        HTML5 Index
    '''

    def get(self):
        self.render('index.html', test="Outbound Campaigns")

if __name__ == '__main__':
    '''
        Howler outbound campaigns
    '''
    opts = options.options()

    db = motor.MotorClient().howler

    if opts.ensure_indexes:
        logging.info('Ensuring indexes...')
        indexes.ensure_indexes(db)
        logging.info('DONE.')

    base_url = opts.base_url

    application = web.Application(

        [
            (r'/', IndexHandler),
            (r'/outbound/?', outbound.Handler)
        ],

        db=db,
        domain=opts.domain,
        page_size=opts.page_size,
        max_retries=opts.max_retries,
        retry_time=opts.retry_time,
        wait_time=opts.wait_time,
        max_calls=opts.max_calls,
        spool_dir=opts.spool_dir,
        tmp_dir=opts.tmp_dir,
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )

    # Setting up server process
    application.listen(opts.port)
    logging.info('Listening on http://%s:%s' % (opts.host, opts.port))
    ioloop.IOLoop.instance().start()
    '''
        [
            https://www.youtube.com/watch?v=9gpmjSHZTiw,
            https://www.youtube.com/watch?v=Ma27diEPqB0,
            https://www.youtube.com/watch?v=WrXwXuhRo9Q
        ]
    '''