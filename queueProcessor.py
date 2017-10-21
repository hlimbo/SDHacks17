from auth_key import *
from twilio.rest import Client
import queue

pThreshold = 50000
pCostPerMessage = 10000

# lower values are higher priority in pq in python
# driftingbottles is queue that holds a collection of tuples
def processQueue(messages, users):
    for user in users.keys():
        users[user] += 1 #age priority every tick

    if len(users) > 0:
        client = Client(account_sid, auth_token)
        recipient = max(users.items(), key=lambda x:x[1])[0]
        print(recipient)
        print(users[recipient])
        try:
            message = messages.get(block=False)
            print(message)
            
            if users[recipient] >= pThreshold:
                if recipient == message[0]:
                    messages.put(message,block=False)
                else:
                    print("SMS sent")
                    client.messages.create(to=recipient,from_=myNumber,body=message[1])
                    users[recipient] -= pCostPerMessage
            else:
                messages.put(message,block=False)
        except:
            pass
    #return 2 queues, 1st queue drifting bottles queue, 2nd dict of the users
    return messages,users
