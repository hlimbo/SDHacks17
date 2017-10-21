from auth_key import *
from twilio.rest import Client
import queue

pThreshold = 50000
pCostPerMessage = 10000
poolSizeBeforeSend = 5

def processQueue(messages, users):
    for user in users.keys():
        users[user] += 1 #age priority every tick

    if len(users) > 0 and messages.qsize() >= 5:
        client = Client(account_sid, auth_token)
        recipient = max(users.items(), key=lambda x:x[1])[0]
        
        try:
            message = messages.get(block=False)
            
            if users[recipient] >= pThreshold:
                if recipient == message[0]:
                    messages.put(message,block=False)
                else:
                    client.messages.create(to=recipient,from_=myNumber,body=message[1])
                    users[recipient] -= pCostPerMessage
            else:
                messages.put(message,block=False)
        except:
            pass

    return messages,users
