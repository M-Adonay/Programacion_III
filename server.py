from http import server
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
import json

class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return SimpleHTTPRequestHandler.do_GET(self)

print ("Servidor Iniciado")
server = HTTPServer(("localhost", 3000), servidorBasico)
server.serve_forever()