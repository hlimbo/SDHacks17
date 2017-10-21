
# prints a list of messages (message log)
from twilio.rest import Client
from auth_key import *

client = Client(account_sid,auth_token)

#print("account_sid:",client.account_sid)
#print("auth:",client.auth)
#print("password:",client.password)

print("pricing:", client.pricing)

# message is a type of resource
#message.body gives you the message sent from phone

for message in client.messages.list():
	# this retrieves the message from specified message id
	#the_message_text = client.messages(message.sid).fetch()
	#print(message.body.encode('utf-8'))
	print(message.direction.encode('utf-8'), ":", message.body.encode('utf-8'))
	print("From:",message.from_)
	print("To:",message.to)
