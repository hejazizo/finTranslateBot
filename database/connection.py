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
	def __init__(self):
		
		self._config = config.DATABASE_CONFIG
		self._conn = psycopg2.connect(self._config['url'])
		self._cur = self._conn.cursor()

	# --------------- Query Wrapper --------------- #
	def create_table(self, table_name, schema):
		
		columns_clause = []
		for column, info in schema.items():
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
		if not isinstance(columns_target, list):
			raise TypeError('columns_target should be a list[]')

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
	
	def select_one(self, table, columns_target=None, conditions=None):
		result = self.select(table=table, columns_target=columns_target, conditions=conditions)

		if result:
			if len(columns_target) == 1: 	return result[0][0]
			else: 							return result[0]
		
		return None
	
	def update(self, table, update_target=None, conditions=None, returnings=None):
		# COLUMNs
		update_clause = self.create_update(updates=update_target)
		# WHERE clause
		where_clause = self.create_where(conditions)
		# Returning clause
		returning_clause = self.create_returning(returnings)
		# QUERY

		self._cur.execute('''
			UPDATE {table} SET {update_clause} {where_clause} {returning_clause}
			'''.format(update_clause=update_clause,
				table = table,
				where_clause=where_clause,
				returning_clause=returning_clause))

		self._conn.commit()

		if returnings:
			results = self._cur.fetchall()
			return results
		

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

	def create_update(self, updates):
		# WHERE clause
		update_clause = ''
		if updates:
			updates_list = []
			for column, value in updates.items():
				
				if isinstance(value, str):
					value = "'{}'".format(value)
				updates_list.append('{}={}'.format(column, value))
			
			update_clause += ', '.join(updates_list)

		return update_clause

	def create_returning(self, returnings):
		#Returning clause
		returning_clause = ''

		if returnings:
			returning_clause += 'RETURNING '
			returnings += ', '.join(returnings)

		return returning_clause