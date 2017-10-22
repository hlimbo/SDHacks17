import http.server
import urllib.parse
import queueProcessor
from auth_key import *
from twilio.rest import Client

serverAddress, serverPort = ("", 18888)
driftingBottles = []
users = dict()
keywords = {"STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT", "START", "YES", "UNSTOP", "HELP", "INFO"}

startingP = 60000
pPerSend = 2500

class TwilioRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        client = Client(account_sid, auth_token)

        try:
            bodyLength = int(self.headers["Content-Length"])
            requestBody = self.rfile.read(bodyLength).decode("utf-8").split("&")
            twilioRequest = dict({tuple(i.split("=")) for i in requestBody})
            
            sender = urllib.parse.unquote_plus(twilioRequest["From"],"utf-8")
            body = urllib.parse.unquote_plus(twilioRequest["Body"],"utf-8")
            
            if body.upper() == "JOIN":
                if sender not in users:
                    users[sender] = startingP
                    client.messages.create(to=sender,from_=myNumber,body="You just joined!")
                else:
                    client.messages.create(to=sender,from_=myNumber,body="You already joined!")
            elif body.upper() not in keywords:
                if sender not in users:
                    users[sender] = startingP
                    client.messages.create(to=sender,from_=myNumber,body="You just joined!")
                driftingBottles.append((sender,body))
                users[sender] += pPerSend
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
