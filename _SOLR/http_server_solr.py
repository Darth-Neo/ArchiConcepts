import SimpleHTTPServer
import SocketServer

PORT = 8000

#  class SimpleHTTPServer.SimpleHTTPRequestHandler(request, client_address, server)
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("127.0.0.1", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
