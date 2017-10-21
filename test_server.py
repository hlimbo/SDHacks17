import http.server
import queue
import urllib.parse
import queueProcessor

serverAddress, serverPort = ("", 18888)
driftingBottles = queue.Queue()
users = dict()
keywords = {"STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT", "START", "YES", "UNSTOP", "HELP", "INFO", "JOIN"}

startingP = 60000
pPerSend = 2500

class TwilioRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            bodyLength = int(self.headers["Content-Length"])
            requestBody = self.rfile.read(bodyLength).decode("utf-8").split("&")
            twilioRequest = dict({tuple(i.split("=")) for i in requestBody})
            twilioRequest["From"] = urllib.parse.unquote_plus(twilioRequest["From"],"utf-8")
            twilioRequest["Body"] = urllib.parse.unquote_plus(twilioRequest["Body"],"utf-8")
            if twilioRequest["From"] not in users:
                users[twilioRequest["From"]] = startingP
            if twilioRequest["Body"].upper() not in keywords:
                driftingBottles.put((twilioRequest["From"],twilioRequest["Body"]),block=False)
                users[twilioRequest["From"]] += pPerSend
            self.send_response(204) #no content
        except:
            self.send_error(418) #teapot!
        finally:
            self.end_headers()

daemon = http.server.HTTPServer((serverAddress, serverPort), TwilioRequestHandler)
daemon.timeout = 1 #in seconds
while True:
    daemon.handle_request()
    driftingBottles,users = queueProcessor.processQueue(driftingBottles,users)
