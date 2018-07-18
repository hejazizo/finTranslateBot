import telebot
import os
import sys
import emoji

from finglish import f2p
from utils.translation import translate

# Creating BOT
TOKEN = os.environ["BEHNEVIS_BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

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
@bot.message_handler(func = lambda message: True)
def fin2persian(message):
	translated_msg = translate(message)
	if translated_msg:
		bot.send_message(message.chat.id, translated_msg, parse_mode='HTML')

# ------------------- Starting BOT ------------------ #
print('BOT IS RUNNING NOW...')
bot.skip_pending = True
bot.polling(none_stop=True)