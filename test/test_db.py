import pytest

def test_select(DB):
	# TABLE name
	chat_id=73106435
	table_name = '{}_{}'.format('EditMsg', chat_id)

	results = DB.select(table=table_name, columns_target=['tel_id', 'bot_msg_id'], conditions={'tel_id': chat_id})
	
	DB.update(table=table_name, update_target={'tel_id': 9999999}, conditions={'tel_id': chat_id})
	print(results)