import os

import tornado.options

from tornado.options import parse_config_file

# ownership missing

config_path = 'spider.conf'

def options():
    '''
        Inbound campaigns configuration options
    '''
    tornado.options.define('ensure_indexes', 
        default=True, type=bool,
        help=('Ensure collection indexes'))

    # Set config and stuff
    tornado.options.define('config',
        type=str, help='path to config file',
        callback=lambda path: parse_config_file(path, final=False))

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

    # MongoDB database settings
    tornado.options.define('mongo_host',
        type=str, help=('MongoDB hostname or ip address'))

    tornado.options.define('mongo_port',
        default=27017, type=int,
        help=('MongoDB port'))

    # PostgreSQL database settings
    tornado.options.define('sql_host',
        type=str, help=('PostgreSQL hostname or ip address'))

    tornado.options.define('sql_port',
        default=5432, type=int,
        help=('PostgreSQL port'))

    tornado.options.define('sql_database',
        type=str, help=('PostgreSQL database'))

    tornado.options.define('sql_user',
        type=str, help=('PostgreSQL username'))

    tornado.options.define('sql_password',
        type=str, help=('PostgreSQL username password'))

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
        help=('Inbound calling retry time'))

    tornado.options.define('wait_time',
        default=45, type=int,
        help=('Wait time'))

    tornado.options.define('max_calls',
        default=10, type=int,
        help=('Maximum number of concurrent calls'))

    tornado.options.define('spool_dir',
        default='/var/spool/asterisk/inbound/', type=str,
        help=('Asterisk inbound spool dir'))

    tornado.options.define('tmp_dir',
        default='/tmp/', type=str,
        help=('tmp inbound stuff'))

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