#- * -coding: utf - 8 - * -
import telebot
import os
import sys
from finglish import f2p
import langid
import emoji

def isEnglish(s):
	try:
		s.encode(encoding = 'utf-8').decode('ascii')
	except UnicodeDecodeError:
		return False
	else:
		return True

languages_list = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 
					'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu', 'he', 'hi', 'hr', 
					'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 
					'mr', 'ne', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 
					'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 
					'uk', 'ur', 'vi', 'zh-cn', 'zh-tw']

# init
TOKEN = os.environ["BEHNEVIS_BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
	welcome_message = "Salam! \nmatn be finglish vared konid."
	bot.reply_to(message, welcome_message)
	bot.send_message(chat_id = message.from_user.id, text = f2p(welcome_message))

@bot.message_handler(func = lambda message: True)
def echo_all(message):
	msg_text = emoji.demojize(message.text)
	language = langid.classify(msg_text)
	print('Language: ', language, 'Message:', msg_text)
	if isEnglish(msg_text) and not msg_text.startswith(':'):
		name = message.from_user.first_name
		if message.from_user.last_name:
			name += ' ' + message.from_user.last_name
		username = message.from_user.username

		output_message = '<b>{name}</b> (@{username}):\n\n{message}'.format(name = name, username = username, message=f2p(message.text))
		bot.send_message(message.from_user.id, output_message, parse_mode='HTML')

print('BOT IS RUNNING NOW...')
bot.skip_pending = True
bot.polling(none_stop=True)