# config.py
import os

DATABASE_CONFIG = {
    'host'		: os.environ['FINBOT_HOST'],
    'dbname'	: os.environ['FINBOT_DB'],
    'user'		: os.environ['FINBOT_USERNAME'],
    'password'	: os.environ['FINBOT_PASS'],
    'port'		: os.environ['FINBOT_PORT'],
	'url'		: os.environ['FINBOT_URL']
}
