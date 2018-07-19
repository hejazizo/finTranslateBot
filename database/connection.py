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
	def __init__(self, dbname=config.DATABASE_CONFIG['dbname']):
		
		self._config = config.DATABASE_CONFIG

		# Connection to Database
		if dbname != self._config['dbname']:
			raise ValueError("Couldn't not find DB with given name")
		self._conn = psycopg2.connect(self._config['url'])
		self._cur = self._conn.cursor()

	# --------------- Query Wrapper --------------- #
	def create_table(self, table_name, columns_info):
		columns_clause = []
		for column, info in columns_info.items():
			columns_clause.append(' '.join([column, info]))
		
		columns_clause = ', '.join(columns_clause)
		self._cur.execute('''
		CREATE TABLE IF NOT EXISTS {table} ({columns})
		'''.format(table=table_name, columns=columns_clause))
		self._conn.commit()

	def drop_table(self, table_name):
		self._cur.execute('''
		DROP TABLE {table}'''.format(table=table_name))
		self._conn.commit()

	def insert(self, table, columns_val):
		columns = '({})'.format(', '.join([str(val) for val in columns_val.keys()]))
		values = '({})'.format(', '.join(['%s' for val in columns_val.keys()]))
		self._cur.execute('''
		INSERT INTO {table_name} {columns} VALUES {values}
		'''.format(table_name=table, 
			columns=columns,
			values=values), tuple(columns_val.values()))

		self._conn.commit()

	def delete(self, table, conditions=None):
		where_clause = self.create_where(conditions)
		self._cur.execute('''
			DELETE FROM {table} {where_clause}'''
			.format(table=table, where_clause=where_clause))
		self._conn.commit()

	def select(self, table, columns_target=None, conditions=None):
		"""
		Queries DB:
			Select columns_target FROM table WHERE conditions

		Args:
			- table (str):
				- EditMsg
				- Users
				- ...
			- columns_target (list[])
			- conditions (dict{})

		Returns:
			- results (list[set()])
				- [(col_1, col_2, col_3), (..., ..., ...), ...]
		"""

		# COLUMNs
		select_clause = self.create_select(columns_target=columns_target)
		# WHERE clause
		where_clause = self.create_where(conditions)
		# QUERY

		self._cur.execute('''
			SELECT {select_clause} FROM {table} {where_clause}
			'''.format(select_clause=select_clause,
				table = table,
				where_clause=where_clause))

		return self._cur.fetchall()


	def create_select(self, columns_target):
		select_clause = '*'
		# COLUMNs
		if columns_target:
			select_clause = ', '.join(columns_target)
		
		return select_clause
		
	def create_where(self, conditions):
		# WHERE clause
		where_clause = ''
		if conditions:
			conditions_list = []
			for column, value in conditions.items():
				
				if isinstance(value, str):
					value = "'{}'".format(value)
				conditions_list.append('{}={}'.format(column, value))
			
			where_clause = 'WHERE '
			where_clause += ' AND '.join(conditions_list)

		return where_clause
