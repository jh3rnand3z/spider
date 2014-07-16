import os

import tornado.options

# ownership missing

config_path = 'howler.conf'

def options():
    '''
        Outbound campaigns configuration options
    '''
    tornado.options.define('ensure_indexes', 
        default=True, type=bool,
        help=('Ensure collection indexes'))

    tornado.options.define('domain',
        default='iofun.io', type=str,
        help='Application domain, e.g: "example.com"')

    # Server settings
    tornado.options.define('host', 
        default='127.0.0.1', type=str,
        help=('Server hostname'))

    tornado.options.define('port',
        default=8888, type=int,
        help=('Server port'))

    tornado.options.define('base_url',
        default='api', type=str,
        help=('Base url, e.g. "api"'))

    tornado.options.define('page_size',
        default=30, type=int,
        help=('Set a custom page size up to 100'))

    tornado.options.define('max_retries',
        default=2, type=int,
        help=('Max retries'))
    
    tornado.options.define('retry_time',
        default=300, type=int,
        help=('Outbound calling retry time'))

    tornado.options.define('wait_time',
        default=45, type=int,
        help=('Wait time'))

    tornado.options.define('max_calls',
        default=10, type=int,
        help=('Maximum number of concurrent calls'))

    tornado.options.define('spool_dir',
        default='/var/spool/asterisk/outgoing/', type=str,
        help=('Asterisk spool dir'))

    tornado.options.define('tmp_dir',
        default='/tmp/', type=str,
        help=('tmp outbound call files'))

    # Parse config file, then command line...
    # so command line switches take precedence
    if os.path.exists(config_path):
        print('Loading', config_path)
        tornado.options.parse_config_file(config_path)
    else:
        print('No config file at', config_path)

    tornado.options.parse_command_line()
    result = tornado.options.options

    for required in (
        'domain', 'host', 'port', 'base_url',
    ):
        if not result[required]:
            raise Exception('%s required' % required)

    return result