import telebot
import os
from collections import defaultdict

from finglish import f2p
from utils.translation import translate
from database.connection import DBConnection

# Creating BOT
TOKEN = os.environ["FINBOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)
DB = DBConnection()


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

	bot_msg_id = DB.select_bot_msg_id(tel_id=message.from_user.id, user_msg_id=message.message_id)
	if bot_msg_id:
		translated_msg = translate(message)
		if translated_msg:
			bot.edit_message_text(translated_msg, message.chat.id, bot_msg_id, parse_mode='HTML')
		else:
			bot.edit_message_text('Message Edited to NON-Finglish.', message.chat.id, bot_msg_id, parse_mode='HTML')
	

@bot.message_handler(func = lambda message: True)
def fin2persian(message):

	translated_msg = translate(message)
	if translated_msg:
		output_message = bot.send_message(message.chat.id, translated_msg, parse_mode='HTML')
		DB.add_msg(tel_id=message.from_user.id, user_msg_id=message.message_id, bot_msg_id=output_message.message_id)

# ------------------- Starting BOT ------------------ #
bot.skip_pending = True
bot.polling(none_stop=True)
print('BOT IS RUNNING NOW...')