# server_test.py
  # Our http server handler for http requests
import SocketServer  # Establish the TCP Socket connections

from SimpleHTTPServer import SimpleHTTPRequestHandler

PORT = 9000


class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'create_sub_task_original.html'
        return SimpleHTTPRequestHandler.do_GET(self)


Handler = MyHttpRequestHandler

with SocketServer.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()