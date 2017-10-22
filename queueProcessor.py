from auth_key import *
from twilio.rest import Client
import random

pThreshold = 30000
pCostPerMessage = 10000
poolSizeBeforeSend = 5

def processQueue(messages, users):
    for user in users.keys():
        print('#:', user, 'priority:', users[user].priority, 'count:', users[user].numMessages)
        users[user].priority += 1 #age priority every tick

    if len(users) > 0 and len(messages) >= poolSizeBeforeSend:
        client = Client(account_sid, auth_token)

        recipient = max(users.items(), key=lambda x:x[1].priority)[0]
        print('recipient:')
        
        try:
            message = messages[0]
            print(message)
            if users[recipient].priority >= pThreshold:
                if recipient != message[0]:
                    client.messages.create(to=recipient,from_=myNumber,body=message[1])
                    users[recipient].priority -= pCostPerMessage
                    users[recipient].numMessages -= 1
                    messages = messages[1:]
                else:
                    messages = messages[1:]
                    random.shuffle(messages)
                    messages.append(message)
            print(messages)
        except:
            pass

    return messages,users
