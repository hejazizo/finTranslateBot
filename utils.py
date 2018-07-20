def postprocess_msg(message, translated_msg):
	# user info appended to translated message
	name = message.from_user.first_name
	if message.from_user.last_name:
		name += ' ' + message.from_user.last_name
	name = '<b>{}</b>'.format(name)

	if message.from_user.username:
		name += ' (@{})'.format(message.from_user.username)

	output_message = '{name}:\n\n{message}'.format(name = name, message=translated_msg)

	return output_message