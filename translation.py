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
	msg_text = message.text
	raw_text = emoji.demojize(msg_text)
	output_message = None

	# 1
	if isEnglish(raw_text) and not emoji.demojize(raw_text).startswith(':'):


		# Result
		# processing multiple line message
		translated_msg = []
		splitted_msg = msg_text.split('\n')
		for msg in splitted_msg:
			translated_msg.append(f2p(msg))
		
		output_message = '\n'.join(translated_msg)
	
	return output_message
