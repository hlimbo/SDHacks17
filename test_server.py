import http.server
import urllib.parse
import queueProcessor
from auth_key import *
from twilio.rest import Client

serverAddress, serverPort = ("", 18888)
driftingBottles = []
users = {}
keywords = {"STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT", "START", "YES", "UNSTOP", "HELP", "INFO"}

startingP = 60000
pPerSend = 2500

class User:
    def __init__(self, priority, numMessages):
        super(User, self).__init__()
        self.priority = priority
        self.numMessages = numMessages
        

class TwilioRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        client = Client(account_sid, auth_token)

        try:
            bodyLength = int(self.headers["Content-Length"])
            requestBody = self.rfile.read(bodyLength).decode("utf-8").split("&")
            twilioRequest = dict({tuple(i.split("=")) for i in requestBody})
            
            sender = urllib.parse.unquote_plus(twilioRequest["From"],"utf-8")
            body = urllib.parse.unquote_plus(twilioRequest["Body"],"utf-8")
            
            if body.upper() not in keywords:
                
                if sender not in users:
                    users[sender] = User(priority = startingP, numMessages = 1)
                    client.messages.create(to=sender,from_=myNumber,body="You just joined!")
                else:
                    if users[sender].numMessages < 5:
                        users[sender].priority += pPerSend
                        users[sender].numMessages += 1
                        driftingBottles.append((sender,body))
                    else:
                        client.messages.create(to=sender,from_=myNumber,body="You have sents in too many texts")                        

            self.send_response(204) #no content
        except Exception as ex:
            print(ex)
            self.send_error(418) #teapot!
        finally:
            self.end_headers()


daemon = http.server.HTTPServer((serverAddress, serverPort), TwilioRequestHandler)
daemon.timeout = 1 #in seconds
while True:
    daemon.handle_request()
    driftingBottles,users = queueProcessor.processQueue(driftingBottles,users)

