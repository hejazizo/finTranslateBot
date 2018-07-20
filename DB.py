#- * -coding: utf - 8 - * -
from database.connection import DBConnection

class DB(object):

	def __init__(self):
		self._db = DBConnection()
		
		editMsg_schema = {
						'tel_id'		: 'INTEGER',
						'user_msg_id'	: 'INTEGER',
						'bot_msg_id'	: 'INTEGER',
						'date'			: 'INTEGER'
						}

		group_schema = {'id'			: 'INTEGER NOT NULL UNIQUE',
						'name'			: 'TEXT',
						'type'			: 'TEXT',
						'all_memebers_are_admin' 	: 'BOOLEAN',
						'counter' 		: 'INTEGER'
					}
		
		user_schema = {
					'id'		: 'INTEGER NOT NULL UNIQUE',
					'name'		: 'TEXT',
					'user_name' : 'TEXT',
					'counter'	: 'INTEGER'
					}
		
		self._db.create_table(table_name='EditMsg', schema=editMsg_schema)
		self._db.create_table(table_name='Groups', schema=group_schema)
		self._db.create_table(table_name='Users', schema=user_schema)

	def add_msgId(self, table, message, bot_message):

		msg_info = {'tel_id' : message.from_user.id, 
					'user_msg_id' : message.message_id, 
					'bot_msg_id' : bot_message.message_id,
					'date' : message.date}
		self._db.insert(table=table, columns_val=msg_info)

	def get_botMsgId(self, table, message):
		msg_info = {'tel_id' : message.from_user.id, 
					'user_msg_id' : message.message_id}

		botMsgId = self._db.select_one(table=table, columns_target=['bot_msg_id'], conditions=msg_info)
		return botMsgId
	
	def update_group(self, message):
		conditions={'id' : message.chat.id}
		group_id = self._db.select_one(table='Groups', columns_target=['id'], conditions=conditions)

		if group_id:
			counter = self._db.select_one(table='Groups', columns_target=['counter'], conditions=conditions)
			update_target = {
						'name' : message.chat.title,
						'type' : message.chat.type,
						'all_memebers_are_admin' : message.chat.all_members_are_administrators,
						'counter' : counter + 1}
			self._db.update(table='Groups', update_target=update_target, conditions=conditions)

		else:
			msg_info = {'id' : message.chat.id, 
						'name' : message.chat.title,
						'type' : message.chat.type,
						'all_memebers_are_admin' : message.chat.all_members_are_administrators,
						'counter' : 1}
			self._db.insert(table='Groups', columns_val=msg_info)


	def update_user(self, message):
		conditions={'id' : message.from_user.id}
		user_id = self._db.select_one(table='Users', columns_target=['id'], conditions=conditions)

		if user_id:
			counter = self._db.select_one(table='Users', columns_target=['counter'], conditions=conditions)
			
			first_name = message.from_user.first_name
			last_name = message.from_user.last_name
			name = '{}{}'.format(first_name, last_name+' ' if last_name else '')
			
			update_target = {
						'name' : name,
						'user_name' : message.from_user.username,
						'counter' : counter + 1}
			self._db.update(table='Users', update_target=update_target, conditions=conditions)

		else:
			msg_info = {'id' : message.from_user.id, 
						'name' : message.chat.title,
						'user_name' : None,
						'counter' : 1}
			self._db.insert(table='Users', columns_val=msg_info)

	
	def update_msg_ids(self,message):
		"""
		This function removes expired message ids.
		"""
		current_date = message.date
		two_day = 2 * 24 * 60 * 60
		two_day = 5
		self._db._cur.execute('''
			DELETE FROM EditMsg WHERE (%s) - date > (%s)
		''', (current_date, two_day))

