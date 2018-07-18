#- * -coding: utf - 8 - * -
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

				<translated_message>
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
		name = '<b>{}</b>'.format(name)

		if message.from_user.username:
			name += ' (@{})'.format(message.from_user.username)

		# Result
		# processing multiple line message
		translated_msg = []
		splitted_msg = msg_text.split('\n')
		for msg in splitted_msg:
			translated_msg.append(f2p(msg))
		
		output_message = '\n'.join(translated_msg)
		output_message = '{name}:\n\n{message}'.format(name = name, message=output_message)
	
	return output_message
