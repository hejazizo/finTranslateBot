import os
import psycopg2
from database import config

class DBConnection(object):
	"""
	Attributes:
		- self._conn		: 	connection to postgreSQL
		- self._cur		: 	currsor of connection
		- self._config	: 	Database config dictionary (dict{})
	"""
	def __init__(self, dbname=config.DATABASE_CONFIG['dbname'], table=config.DATABASE_CONFIG['table']):
		
		self._config = config.DATABASE_CONFIG
		self._table = table

		# Connection to Database
		if dbname != self._config['dbname']:
			raise ValueError("Couldn't not find DB with given name")
		self._conn = psycopg2.connect(host=self._config['host'],
							user=self._config['user'],
							password=self._config['password'],
							dbname=self._config['dbname'],
							port=self._config['port'])
		self._cur = self._conn.cursor()

		# Create Database Tables
		self.create_tables()
	
	def create_tables(self):
		self._cur.execute('''
		CREATE TABLE IF NOT EXISTS {table}(
			tel_id INTEGER,
			user_msg_id INTEGER,
			bot_msg_id INTEGER
		)
		'''.format(table=self._table))
		self._conn.commit()

	def add_msg(self, tel_id, user_msg_id, bot_msg_id):
		"""
		Adds the information of one translated message

		       User      |  User Message   | Translated Message
		-------------------------------------------------------
		user telegram id | user message id |   bot message id
		
		"""
		self._cur.execute('''
		INSERT INTO {table} (tel_id, user_msg_id, bot_msg_id) VALUES (%s, %s, %s)
		'''.format(table=self._table), (tel_id, user_msg_id, bot_msg_id))
		self._conn.commit()

	def select_bot_msg_id(self, tel_id, user_msg_id):
		"""
		Retrieves the translated message id from DB by having:
			- User Telegram ID
			- User Message ID
		"""
		self._cur.execute('''
		SELECT bot_msg_id FROM {table} WHERE tel_id = (%s) AND user_msg_id = (%s)
		'''.format(table=self._table), (tel_id, user_msg_id))
		bot_msg_id = self._cur.fetchone()

		return bot_msg_id

	def del_msg(self, tel_id, user_msg_id, bot_msg_id):
		self._cur.execute('''
		DELETE FROM {table} WHERE tel_id = (%s) AND 
									user_msg_id = (%s) AND 
									bot_msg_id = (%s)'''.format(table=self._table), 
									(tel_id, user_msg_id, bot_msg_id))
		self._conn.commit()