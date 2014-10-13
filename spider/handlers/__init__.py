from tornado import gen
from tornado import web

from spider.tools import errors


class BaseHandler(web.RequestHandler):
    '''
        System application request handler

        gente d'armi e ganti
    '''

    def initialize(self, **kwargs):
        '''
            Initialize the Base Handler
        '''
        super(BaseHandler, self).initialize(**kwargs)

        # System database
        self.db = self.settings['db']

        # Page settings
        self.page_size = self.settings['page_size']

        # Call file settings
        self.max_retries = self.settings['max_retries'] 
        self.retry_time = self.settings['retry_time']
        self.wait_time = self.settings['wait_time']

        # outbound settings
        self.max_calls = self.settings['max_calls']
        self.spool_dir = self.settings['spool_dir']
        self.tmp_dir = self.settings['tmp_dir']

    def set_default_headers(self):
        '''
            Mango default headers
        '''
        self.set_header("Access-Control-Allow-Origin", self.settings['domain'])

    @gen.engine
    def let_it_crash(self, struct, model, error, reason, callback):
        '''
            Let it crash.
        '''

        str_error = str(error)
        error_handler = errors.Error(error)
        messages = []

        if error and 'Model' in str_error:
            message = error_handler.model(model)

        elif error and 'duplicate' in str_error:
            # messages = []
            for name, value in reason.get('duplicates'):

                message = error_handler.duplicate(
                    name.title(),
                    value,
                    struct.get(value)
                )

                messages.append(message)
            
            message = ({'messages':messages} if messages else False)

        elif error and 'value' in str_error:
            message = error_handler.value()

        elif error is not None:
            print(type(error))
            print(error)
            print('WARNING: ', str_error, ' random nonsense.') 

            message = {
                'error': u'nonsense',
                'message': u'there is no error'
            }

        else:
            
            message = {
                'status': 200,
                'message': 'get this shit out'
            }

        callback(message, None)

    @gen.engine
    def new_in_queue(self, struct, callback):
        '''
            New inbound queue
        '''

        '''

        insert into queues (
            name,
            musiconhold,
            context,
            timeout,
            monitor_join,
            monitor_format,
            queue_youarenext,
            queue_lessthan,
            queue_thankyou,
            queue_reporthold,
            announce_frequency,
            announce_round_seconds,
            retry,
            wrapuptime,
            maxlen,
            servicelevel,
            strategy,
            joinempty,
            reportholdtime,
            periodic_announce,
            periodic_announce_frequency,
            ringinuse,
            setinterfacevar
        ) values (
            'gocella',
            'default',
            'dialplan_gocella',
            15,
            True,
            'wav',
            'queue-youarenext',
            'queue-less-than',
            'queue-thankyou',
            'queue-reporthold',
            0,
            10,
            1,
            5,
            0,
            0,
            'rrmemory',
            1,
            True,
            'gocella/periodic_announce',
            25,
            False,
            True
        );

        '''

        try:
            query = '''
                insert into sip (
                    name,
                    defaultuser,
                    fromuser,
                    fromdomain,
                    host,
                    sippasswd,
                    allow,
                    context,
                    avpf,
                    encryption
                ) values (
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    'dynamic',
                    '%s',
                    'g729,gsm,alaw,ulaw',
                    'fun-accounts',
                    'no',
                    'no'
                );
            ''' % (struct['account'],
                   struct['account'],
                   struct['account'],
                   self.settings['domain'],
                   struct['password'])

            cursor = yield momoko.Op(self.sql.execute, query)

        except (psycopg2.Warning, psycopg2.Error) as error:
            print('WARNING: ', str(error))
            callback(None, str(error))
            return
        else:
            result = True

        callback(result, None)