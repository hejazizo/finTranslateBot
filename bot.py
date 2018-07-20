import telebot
import os
from collections import defaultdict

from finglish import f2p
from translation import translate
from DB import DB
from utils import postprocess_msg

DBhandler = DB()

# Creating BOT
TOKEN = os.environ["FINBOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

UPDATE_COUNTER = 0

# ------------ /start and /help commands ------------ #
@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
	"""
	/start and /help commands messages.
	"""
	welcome_message = "Salam! matn be finglish vared konid."
	welcome_message += '\n{}'.format(f2p(welcome_message))
	bot.send_message(chat_id = message.chat.id, text = welcome_message)

# --------------- Translation function -------------- #
@bot.edited_message_handler(func = lambda message: True)
def edited_message(message):
	"""
	Edits the translated message if user edits the message.

	NOTE: if user edits the message to non-finglish, 
			message will be edited to: 'Message Edited to NON-Finglish.'
	"""

	try:
		print('HERE')
		# TABLE: EditMsg
		bot_MsgId = DBhandler.get_botMsgId(table='EditMsg', message=message)
		print(bot_MsgId)
		if bot_MsgId:
			print('HERE _ 2')
			translated_msg = translate(message)
			if translated_msg:
				translated_msg = postprocess_msg(message, translated_msg)
				bot.edit_message_text(translated_msg, message.chat.id, bot_MsgId, parse_mode='HTML')
			else:
				bot.edit_message_text('Message Edited to NON-Finglish.', message.chat.id, bot_MsgId, parse_mode='HTML')
	except Exception as e:
		print(e)

@bot.message_handler(func = lambda message: True)
def fin2persian(message):
	
	try:
		# TABLE: EditMsg, Groups, Users
		translated_msg = translate(message)
		if translated_msg:
			

			translated_msg = postprocess_msg(message, translated_msg)
			bot_message = bot.send_message(message.chat.id, translated_msg, parse_mode='HTML')
			DBhandler.add_msgId(table='EditMsg', message=message, bot_message=bot_message)

			# # Update User and Group Info
			# if message.chat.type == 'group':
			# 	DBhandler.update_group(message)
			# DBhandler.update_user(message)
			# # REMOVING expired messages for edit

			global UPDATE_COUNTER
			UPDATE_COUNTER += 1
			if UPDATE_COUNTER % 200 == 0:
				DBhandler.update_msg_ids(message)
				UPDATE_COUNTER = 0

	except Exception as e:
		print(e)

# ------------------- Starting BOT ------------------ #
bot.skip_pending = True
bot.polling(none_stop=True)
print('BOT IS RUNNING NOW...')