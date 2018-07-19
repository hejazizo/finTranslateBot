from database.connection import DBConnection

class DB(object):

	def __init__(self):
		self._db = DBConnection()
		self._columns_info = {'tel_id': 'INTEGER',
							'user_msg_id': 'INTEGER',
							'bot_msg_id': 'INTEGER'}

	
	def add_msgId(self, table, message, bot_message):
		self._db.create_table(table_name=table, columns_info=self._columns_info)
		
		msg_info = {'tel_id' : message.from_user.id, 
					'user_msg_id' : message.message_id, 
					'bot_msg_id' : bot_message.message_id}
		self._db.insert(table=table, columns_val=msg_info)

	def get_botMsgId(self, table, message):
		msg_info = {'tel_id' : message.from_user.id, 
					'user_msg_id' : message.message_id}

		botMsgId = self._db.select(table=table, columns_target=['bot_msg_id'], conditions=msg_info)

		if botMsgId:
			return botMsgId[0]
		
		return None