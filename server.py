from os import name
import mysql.connector
import json
import datetime
import random
import tensorflow as tf
import pandas as pd
import numpy as np

from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

#Importar el archivo csv
archivo = pd.read_csv("predicciones.csv", sep=";")
tX = archivo.iloc[:,0:4].values
pY = archivo.iloc[:,4:8].values
#Crear el modelo
modelo = tf.keras.Sequential()
#Crear una capa de entrada
modelo.add(tf.keras.layers.Dense(units=4, input_dim=4, activation='relu'))
#Crear una capa de salida
modelo.add(tf.keras.layers.Dense(units=4, activation='sigmoid'))
#Compilar el modelo
modelo.compile(optimizer='adam', loss='mean_squared_error', metrics=['binary_accuracy'])
#Entrenar el modelo
modelo.fit(tX, pY, epochs=100)

prediccion = np.array([[21,23,40,40]])
#Predecir el resultado
prediccion = modelo.predict(prediccion)
real = np.argmax(prediccion)
print(real)

class crud():
    def __init__(self):
        self.sesion = {'inicio': False, 'id':'None', 'usuario':'None', 'contra':'None'}
        self.conn = mysql.connector.connect(host = 'localhost', user = 'root', port = '3307', password = '', database = 'book_store')
        if self.conn.is_connected():
            print('Conectado a la base de datos')
        else:
            print('No se pudo conectar a la base de datos')

    def generar_id(self, tabla):
        # Conseguir el mayor id
        if tabla == 'libros':
            sql = 'SELECT MAX(idLibro) AS id FROM libros'
        elif tabla == 'tipocuenta':
            sql = 'SELECT MAX(idTipo) AS id FROM tipocuenta'
        elif tabla == 'generos':
            sql = 'SELECT MAX(idGenero) AS id FROM generos'
        resultado = self.ejecutar_mostrar_sql(sql)
        if resultado[0] == True:
            id = resultado[1][0]['MAX(id' + tabla + ')']
            if id == None:
                id = 0
            id = int(id) + 1
            return id
        else:
            return False

    def ejecutar_sql(self, sql, valores):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, valores)
            self.conn.commit()
            print('Se ejecuto la consulta')
            return True
        except Exception as e:
            print(e)
            return False

    def ejecutar_mostrar_sql(self, sql):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql)
            resultado = cursor.fetchall()
            if len(resultado) == 0:
                return False, resultado
            else:
                return True, resultado
        except Exception as e:
            print(e)
            return False

    def ejecutar_select_datos(self, sql, datos):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql, datos)
            resultado = cursor.fetchall()
            if len(resultado) == 0:
                return False, resultado
            else:
                return True, resultado
        except Exception as e:
            print(e)
            return False

    def administrar_libros(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO libros (idLibro, Titulo, Autor, Edicion, Sinopsis, Imagen, Cantidad) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            valores = (self.generar_id('libros'), datos['titulo'], datos['autor'], datos['edicion'], datos['sinopsis'], datos['imagen'], datos['cantidad'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE libros SET Titulo = %s, Autor = %s, Edicion = %s, Sinopsis = %s, Imagen = %s, Cantidad = %s WHERE idLibro = %s'
            valores = (datos['titulo'], datos['autor'], datos['edicion'], datos['sinopsis'], datos['imagen'], datos['cantidad'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM libros WHERE idLibro = %s'
            valores = (datos['id'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT libros.idLibro, libros.Titulo, libros.Autor, libros.Edicion, libros.Sinopsis, libros.Imagen, libros.Cantidad, GROUP_CONCAT(generos.Nombre) AS Generos, GROUP_CONCAT(generos.idGenero) AS idGeneros FROM libros LEFT JOIN generolibro ON libros.idLibro = generolibro.idLibro LEFT JOIN generos ON generolibro.idGenero = generos.idGenero GROUP BY libros.idLibro'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_cuentas(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO usuarios (idUsuario, Dui, Nombre, Nickname, Telefono, Correo, Direccion, FechaNacimiento, Contraseña, idTipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            valores = (datos['id'], datos['dui'], datos['nombre'], datos['nickname'], datos['telefono'], datos['correo'], datos['direccion'], datos['fechaNacimiento'], datos['contraseña'], datos['idTipo'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE usuarios SET Dui = %s, Nombre = %s, Nickname = %s, Telefono = %s, Correo = %s, Direccion = %s, FechaNacimiento = %s, Contraseña = %s, idTipo = %s WHERE idUsuario = %s'
            valores = (datos['dui'], datos['nombre'], datos['nickname'], datos['telefono'], datos['correo'], datos['direccion'], datos['fechaNacimiento'], datos['contraseña'], datos['idTipo'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM usuarios WHERE idUsuario = %s'
            valores = (datos['id'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT usuarios.idUsuario, usuarios.Dui, usuarios.Nombre, usuarios.Nickname, usuarios.Telefono, usuarios.Correo, usuarios.Direccion, usuarios.FechaNacimiento, usuarios.Contraseña, usuarios.idTipo, tipocuenta.Descripcion AS Tipo FROM usuarios LEFT JOIN tipocuenta ON usuarios.idTipo = tipocuenta.idTipo'
            # sql = 'SELECT * FROM usuarios'
            return self.ejecutar_mostrar_sql(sql)

        elif datos['accion'] == 'mostrar_a':
            sql = 'SELECT usuarios.idUsuario, usuarios.Dui, usuarios.Nombre, usuarios.Nickname, usuarios.Telefono, usuarios.Correo, usuarios.Direccion, usuarios.FechaNacimiento, usuarios.Contraseña, tipocuenta.idTipo, tipocuenta.Descripcion FROM usuarios LEFT JOIN tipocuenta ON usuarios.idTipo = tipocuenta.idTipo WHERE usuarios.idUsuario = %s'
            valores = (self.sesion['id'],)
            return self.ejecutar_select_datos(sql, valores)

        elif datos['accion'] == 'mostrar_favoritos':
            sql = 'SELECT usuarios.Nombre, GROUP_CONCAT(generos.idGenero) AS Generos FROM usuarios LEFT JOIN librosprestados ON usuarios.idUsuario = librosprestados.idUsuario LEFT JOIN libros ON librosprestados.idLibro = libros.idLibro LEFT JOIN generolibro ON libros.idLibro = generolibro.idLibro LEFT JOIN generos ON generolibro.idGenero = generos.idGenero WHERE usuarios.idUsuario = %s GROUP BY generos.idGenero ORDER BY librosprestados.idPrestado DESC LIMIT 10'
            valores = (self.sesion['id'],)
            resultado = self.ejecutar_select_datos(sql, valores)
            generos = []
            for i in range(len(resultado[1])):
                generos.append(len(resultado[1][i]['Generos'].split(',')))
            print('Longitud en generos')
            print('Longitudes',generos)
            
            if len(generos) < 4:
                for i in range(4-len(generos)):
                    generos.append(0)
            print('Longitudes',generos)
            valores = []
            for i in range(4):
                valores.append(max(generos))
                generos.remove(max(generos))
            # Desordeamos la lista
            random.shuffle(valores)
            print('Valores',valores)
            prediccion = modelo.predict([valores])
            prediccion = np.array(prediccion)
            return resultado[1], prediccion

    def administrar_prestamos(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'UPDATE libros SET Cantidad = Cantidad - 1 WHERE idLibro = %s'
            valores = (datos['idLibro'],)
            self.ejecutar_sql(sql, valores)
            sql = 'INSERT INTO prestamos (idPrestamo, idUsuario, idLibro, FechaPrestamo, FechaDevolusion) VALUES (%s, %s, %s, %s, %s)'
            valores = (datos['id'], datos['idUsuario'], datos['idLibro'], datos['fechaPrestamo'], datos['fechaDevolusion'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE prestamos SET idUsuario = %s, idLibro = %s, FechaPrestamo = %s, FechaDevolusion = %s WHERE idPrestamo = %s'
            valores = (datos['idUsuario'], datos['idLibro'], datos['fechaPrestamo'], datos['fechaDevolusion'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM prestamos WHERE idPrestamo = %s'
            valores = (datos['idPrestamo'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT prestamos.idPrestamo, libros.idLibro, libros.Titulo, usuarios.idUsuario, usuarios.Nombre, tipoCuenta.Descripcion AS Tipo_Cuenta, prestamos.FechaPrestamo, prestamos.FechaDevolusion FROM prestamos INNER JOIN libros ON prestamos.idLibro = libros.idLibro INNER JOIN usuarios ON prestamos.idUsuario = usuarios.idUsuario INNER JOIN tipoUsuario ON usuarios.idTipo = tipoCuenta.idTipo'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_tipo_cuentas(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO tipocuenta (idTipo, Descripcion) VALUES (%s, %s)'
            valores = (datos['id'], datos['descripcion'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE tipocuenta SET Descripcion = %s WHERE idTipo = %s'
            valores = (datos['descripcion'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM tipocuenta WHERE idTipo = %s'
            valores = (datos['id'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT * FROM tipocuenta'
            return self.ejecutar_mostrar_sql(sql)

    def administra_generos(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO generos (idGenero, Nombre, Descripcion) VALUES (%s, %s, %s)'
            valores = (datos['id'], datos['nombre'], datos['descripcion'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE generos SET Nombre = %s, Descripcion = %s WHERE idGenero = %s'
            valores = (datos['nombre'], datos['descripcion'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM generos WHERE idGenero = %s'
            valores = (datos['id'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT * FROM generos'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_estanterias(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO estanteria (idUsuario, idLibro) VALUES (%s, %s)'
            valores = (datos['idUsuario'], datos['idLibro'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE estanteria SET idUsuario = %s, idLibro = %s WHERE idUsuario = %s AND idLibro = %s'
            valores = (datos['idUsuario'], datos['idLibro'], datos['idUsuario'], datos['idLibro'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM estanteria WHERE idUsuario = %s AND idLibro = %s'
            valores = (datos['idUsuario'], datos['idLibro'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT estanteria.idUsuario, estanteria.idLibro, libros.idLibro, libros.Titulo, usuarios.idUsuario, usuarios.Nombre FROM estanteria INNER JOIN libros ON estanteria.idLibro = libros.idLibro INNER JOIN usuarios ON estanteria.idUsuario = usuarios.idUsuario'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_prediccion(self, datos):
        sql = 'SELECT libros.Titulo, generos.Nombre, libro.Autor, libros.Sinopsis, libros.Imagen FROM libros INNER JOIN generolibro ON libros.idLibro = generolibro.idLibro INNER JOIN generos ON generolibro.idGenero = generos.idGenero INNER JOIN autores ON libros.idAutor = autores.idAutor WHERE generos.idGenero = %s'
        valores = (datos['idGenero'],)
        return self.ejecutar_select_datos(sql, valores)

    def registro(self):
        if self.sesion['inicio'] == True:
            return True
        else:
            return False
        
    def salir(self):
        self.sesion['inicio'] = False
        self.sesion['id'] = 'None'
        self.sesion['usuario'] = 'None'
        self.sesion['contra'] = 'None'
        if self.sesion['inicio'] == False:
            return True
        else:
            return False

    def administrar_sesion(self, datos):
        sql = 'SELECT * FROM usuarios WHERE Nickname = %s AND Contraseña = %s'
        valores = (datos['usuario'], datos['contra'])
        resultado = self.ejecutar_select_datos(sql, valores)
        if resultado[0] == True:
            self.sesion['inicio'] = True
            self.sesion['id'] = resultado[1][0]['idUsuario']
            self.sesion['usuario'] = resultado[1][0]['Nickname']
            self.sesion['contra'] = resultado[1][0]['Contraseña']
            return True
        else:
            return False


crud = crud()

class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        #Redirigir para el path /
        if self.path == '/':
            if crud.registro() == True:
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /index
        elif self.path == '/index':
            if crud.registro() == True:
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /login
        elif self.path == '/login':
            if crud.registro() == True:
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /cuenta
        elif self.path == '/cuenta':
            if crud.registro() == True:
                self.path = '/cuenta.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /estanteria
        elif self.path == '/estanteria':
            if crud.registro() == True:
                self.path = '/estanteria.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /recomedaciones
        elif self.path == '/recomendaciones':
            if crud.registro() == True:
                self.path = '/recomendaciones.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /tendencias
        elif self.path == '/tendencias':
            if crud.registro() == True:
                self.path = '/tendencias.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /prestamos
        elif self.path == '/prestamos':
            if crud.registro() == True:
                self.path = '/prestamos.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /libroasad
        elif self.path == '/librosad':
            if crud.registro() == True:
                self.path = '/librosad.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /usuariosad
        elif self.path == '/usuariosad':
            if crud.registro() == True:
                self.path = '/usuariosad.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /prestamosad
        elif self.path == '/prestamosad':
            if crud.registro() == True:
                self.path = '/prestamosad.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/mostrar_libros':
            resultado = crud.administrar_libros({'accion':'mostrar'})
            print(resultado[0])
            for libro in resultado[1]:
                libro['Edicion'] = str(libro['Edicion'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_usuarios_a':
            resultado = crud.administrar_cuentas({'accion':'mostrar_a'})
            print(resultado)
            for usuario in resultado[1]:
                usuario['FechaNacimiento'] = str(usuario['FechaNacimiento'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_usuarios':
            resultado = crud.administrar_cuentas({'accion':'mostrar'})
            print(resultado)
            for usuario in resultado[1]:
                usuario['FechaNacimiento'] = str(usuario['FechaNacimiento'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_recomendaciones':
            resultado = crud.administrar_cuentas({'accion':'mostrar_favoritos'})
            print(resultado[1][0])
            self.send_response(200)
            self.end_headers()
            #Convertir el ndarray en un diccionario
            prediccion = {}
            for i in range(len(resultado[1][0])):
                prediccion[i] = resultado[1][0][i]
            print(prediccion)
            self.wfile.write(json.dumps(prediccion).encode('utf-8'))
            # #Convertir el ndarray a un array normal
            # prediccion = []
            # for recomendacion in resultado[1][0]:
            #     prediccion.append(recomendacion)
            # print(prediccion)
            
            # self.wfile.write(prediccion.encode('utf-8'))
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode('utf-8')
        data = json.loads(data)

        if self.path == '/iniciar_sesion':
            respuesta = crud.administrar_sesion(data)
            if respuesta == True:
                print('Inicio de sesion correcto')
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(dict({'inicio':True})).encode('utf-8'))
            else:
                print('No se ha podido iniciar sesion')

        elif self.path == '/salir':
            respuesta = crud.salir()
            if respuesta == True:
                print('Sesion cerrada')
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(dict({'salir':True})).encode('utf-8'))
            else:
                print('No se ha podido cerrar sesion')

        if self.path == '/administrar_libro':
            respuesta = crud.administrar_libros(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        if self.path == '/administrar_usuarios':
            respuesta = crud.administrar_cuentas(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))


print('Iniciando servidor')
httpd = HTTPServer(('localhost', 3000), servidorBasico)
httpd.serve_forever()