import http.server
import queue
import urllib.parse
#from auth_key import *
import queueProcessor

serverAddress, serverPort = ("", 18888)
driftingBottles = queue.Queue()

class TwilioRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            bodyLength = int(self.headers["Content-Length"])
            requestBody = self.rfile.read(bodyLength).decode("utf-8").split("&")
            twilioRequest = dict({tuple(i.split("=")) for i in requestBody})
            twilioRequest["From"] = urllib.parse.unquote_plus(twilioRequest["From"],"utf-8")
            twilioRequest["Body"] = urllib.parse.unquote_plus(twilioRequest["Body"],"utf-8")
            #print(twilioRequest["From"])
            #print(twilioRequest["Body"])
            driftingBottles.put((twilioRequest["From"],twilioRequest["Body"]),block=False)
            self.send_response(204) #no content
        except:
            self.send_error(418) #teapot!
        finally:
            self.end_headers()

daemon = http.server.HTTPServer((serverAddress, serverPort), TwilioRequestHandler)
daemon.timeout = 1 #in seconds
while True:
    daemon.handle_request()
    #driftingBottles = queueProcessor.processQueue(driftingBottles)

    print("hi")
    try:
        print("a")		
        fromData = driftingBottles.get_nowait()
        print("b")
        print("fromData ",fromData)
    except:
        print("no messages in queue")
        pass	

    print("bye")		
