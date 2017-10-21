import http.server
from auth_key import *

serverAddress, serverPort = ("", 18888)

class TwilioRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            self.send_response(204) #no content
            print(self.requestline)
            bodyLength = int(self.headers["Content-Length"])
            requestBody = self.rfile.read(bodyLength).decode("utf-8").split("&")
            twilioRequest = dict({tuple(i.split("=")) for i in requestBody})
            print(twilioRequest)
        except:
            self.send_error(418) #teapot!
        finally:
            self.end_headers()

daemon = http.server.HTTPServer((serverAddress, serverPort), TwilioRequestHandler)
daemon.serve_forever()
