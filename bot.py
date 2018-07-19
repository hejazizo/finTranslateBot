import telebot
import os
from collections import defaultdict

from finglish import f2p
from translation import translate
from DB import DB

DBhandler = DB()

# Creating BOT
TOKEN = os.environ["FINBOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

try:

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
		CHAT_ID = message.chat.id
		table='EditMsg_{}'.format(CHAT_ID)
		if CHAT_ID < 0:
			CHAT_ID = -1 * CHAT_ID
			table='EditMsg_{}_{}'.format(message.chat.type, CHAT_ID)

		bot_MsgId = DBhandler.get_botMsgId(table=table, message=message)
		if bot_MsgId:
			translated_msg = translate(message)
			if translated_msg:
				bot.edit_message_text(translated_msg, message.chat.id, bot_MsgId, parse_mode='HTML')
			else:
				bot.edit_message_text('Message Edited to NON-Finglish.', message.chat.id, bot_MsgId, parse_mode='HTML')

	@bot.message_handler(func = lambda message: True)
	def fin2persian(message):

		# TABLE: USER
		DBhandler.update_user(message)

		print(message)
		
		# TABLE: EditMsg
		CHAT_ID = message.chat.id
		table='EditMsg_{}'.format(CHAT_ID)
		if CHAT_ID < 0:
			CHAT_ID = -1 * CHAT_ID
			table='EditMsg_{}_{}'.format(message.chat.type, CHAT_ID)
			
		translated_msg = translate(message)
		if translated_msg:
			bot_message = bot.send_message(message.chat.id, translated_msg, parse_mode='HTML')
			DBhandler.add_msgId(table=table, message=message, bot_message=bot_message)

	# ------------------- Starting BOT ------------------ #
	bot.skip_pending = True
	bot.polling(none_stop=True)
	print('BOT IS RUNNING NOW...')

except Exception as e:
	print(e)