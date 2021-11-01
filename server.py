from http import server
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
import json
import mysql.connector
from mysql.connector import Error

class crud:
    def __init__(self):
        print("Iniciando conexion con la base de datos...")
        self.db = mysql.connector.connect(
            host ="localhost",
            user ="root",
            passwd = "",
            database = "db_academica_a2"
        )
        if self.db.is_connected():
            print("Conexion establecida")
        else:
            print("Conexion Fallida")
    
    def insertar(self, codigo, nombre, telefono):
        cursor = self.db.cursor()
        sql = "INSERT INTO alumnos (codigo, nombre, telefono) VALUES (%s, %s, %s)"
        val = (codigo, nombre, telefono)
        cursor.execute(sql, val)
        self.db.commit()
        return "Registro insertado"
crud = crud()


class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_Post(self):
        longitud_contenido = int(self.headers['Content-Length'])
        contenido = self.rfile.read(longitud_contenido)
        contenido = contenido.decode("utf-8")
        contenido = parse.unquote(contenido)
        contenido = json.loads(contenido)
        

print ("Servidor Iniciado")
server = HTTPServer(("localhost", 3000), servidorBasico)
server.serve_forever()