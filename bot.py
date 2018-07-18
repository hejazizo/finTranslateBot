import telebot
import os
import sys
import emoji

from finglish import f2p

## Function to detect non english characters
def isEnglish(s):
	try:
		s.encode(encoding = 'utf-8').decode('ascii')
	except UnicodeDecodeError:
		return False
	else:
		return True


## Main translation function
def translate(message):
	"""
	Function to translate finglish to persian.

	NOTE: #1 These messages are not processed by BOT:
			1. Messages that are not english characters.
			2. Messages that start with emojies.

	TODO: remove emojis from the beginning of a message and then process the rest of it.

	Args:
		message object

	Returns:
		translated message (str)
		------------------------------
			name (@username):

				<translated message>
		------------------------------

		NOTE:
			- name is formatted BOLD
			- if user has no username, output will only include name and <translated message>
	"""

	# removing emojies
	msg_text = emoji.demojize(message.text)

	output_message = None
	# 1
	if isEnglish(msg_text) and not msg_text.startswith(':'):

		# user info appended to translated message
		name = message.from_user.first_name
		if message.from_user.last_name:
			name += ' ' + message.from_user.last_name
		if message.from_user.username:
			name += ' (@{})'.format(message.from_user.username)

		# result
		output_message = '<b>{name}</b>:\n\n{message}'.format(name = name, message=f2p(message.text))
	
	return output_message

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