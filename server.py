from os import name
import mysql.connector
import json
import datetime
import random
import tensorflow as tf
import pandas as pd
import numpy as np
from PIL import Image
from datetime import timedelta

from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

#Importar el archivo csv
archivo = pd.read_csv("predicciones.csv", sep=";")
tX = archivo.iloc[:,0:4].values
pY = archivo.iloc[:,4:8].values
#Crear el modelo
modelo = tf.keras.Sequential()
#Crear una capa de entrada
# modelo.add(tf.keras.layers.Sparc)
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
        print(tabla)
        if tabla == 'libros':
            sql = 'SELECT MAX(idLibro) AS id FROM libros'
        elif tabla == 'tipocuenta':
            sql = 'SELECT MAX(idTipo) AS id FROM tipocuenta'
        elif tabla == 'generos':
            sql = 'SELECT MAX(idGenero) AS id FROM generos'
        elif tabla == 'usuarios':
            sql = 'SELECT MAX(idUsuario) AS id FROM usuarios'
        elif tabla == 'librosprestados':
            sql = 'SELECT MAX(idPrestado) AS id FROM librosprestados'
        resultado = self.ejecutar_mostrar_sql(sql)
        if resultado[0] == True:
            id = resultado[1][0]['id']
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
            id = self.generar_id('libros')
            valores = (id, datos['titulo'], datos['autor'], datos['edicion'], datos['sinopsis'], 'imagenes/portadas/front'+str(id)+'.jpg', datos['cantidad'])
            if self.ejecutar_sql(sql, valores) == True:
                for genero in datos['generos']:
                    sql = 'INSERT INTO generolibro (idLibro, idGenero) VALUES (%s, %s)'
                    valores = (id, genero)
                    self.ejecutar_sql(sql, valores)
                return True, id
            else:
                return False
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE libros SET Titulo = %s, Autor = %s, Edicion = %s, Sinopsis = %s, Imagen = %s, Cantidad = %s WHERE idLibro = %s'
            valores = (datos['titulo'], datos['autor'], datos['edicion'], datos['sinopsis'], datos['imagen'], datos['cantidad'], datos['id'])
            if self.ejecutar_sql(sql, valores) == True:
                sql = 'DELETE FROM generolibro WHERE idLibro = %s'
                valores = (datos['id'],)
                print(type(datos['id']))
                if self.ejecutar_sql(sql, valores) == True:
                    for genero in datos['generos']:
                        sql = 'INSERT INTO generolibro (idLibro, idGenero) VALUES (%s, %s)'
                        valores = (datos['id'], genero)
                        self.ejecutar_sql(sql, valores)
                    return True
            else:
                return False

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM generolibro WHERE idLibro = %s'
            valores = (datos['id'],)
            if self.ejecutar_sql(sql, valores) == True:
                sql = 'DELETE FROM libros WHERE idLibro = %s'
                valores = (datos['id'],)
                if self.ejecutar_sql(sql, valores) == True:
                    return True
                else:
                    return False

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT libros.idLibro, libros.Titulo, libros.Autor, libros.Edicion, libros.Sinopsis, libros.Imagen, libros.Cantidad, GROUP_CONCAT(generos.Nombre) AS Generos, GROUP_CONCAT(generos.idGenero) AS idGeneros FROM libros LEFT JOIN generolibro ON libros.idLibro = generolibro.idLibro LEFT JOIN generos ON generolibro.idGenero = generos.idGenero GROUP BY libros.idLibro'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_cuentas(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO usuarios (idUsuario, Dui, Nombre, Nickname, Telefono, Correo, Direccion, FechaNacimiento, Contraseña, idTipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            id = self.generar_id('usuarios')
            valores = (id, datos['dui'], datos['nombre'], datos['nickname'], datos['telefono'], datos['correo'], datos['direccion'], datos['fechaNacimiento'], datos['contraseña'], datos['idTipo'])
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
            print(self.sesion)
            sql = 'SELECT usuarios.Nombre, GROUP_CONCAT(generos.idGenero) AS Generos FROM usuarios LEFT JOIN librosprestados ON usuarios.idUsuario = librosprestados.idUsuario LEFT JOIN libros ON librosprestados.idLibro = libros.idLibro LEFT JOIN generolibro ON libros.idLibro = generolibro.idLibro LEFT JOIN generos ON generolibro.idGenero = generos.idGenero WHERE usuarios.idUsuario = %s GROUP BY generos.idGenero ORDER BY librosprestados.idPrestado DESC LIMIT 10'
            valores = (self.sesion['id'],)
            resultado = self.ejecutar_select_datos(sql, valores)
            print(resultado)
            generos = []
            etiquetas = []
            if resultado != False:
                if resultado[0]['Generos'] != None:
                    for i in range(len(resultado[1])):
                        generos.append(len(resultado[1][i]['Generos'].split(',')))
                        
            print('Longitud en generos')
            print('Longitudes',generos)
            
            if len(generos) < 10:
                for i in range(10-len(generos)):
                    generos.append(0)
            print('Longitudes',generos)
            valores = []
            # 
            for i in range(4):
                valores.append(max(generos))
                generos.remove(max(generos))
            
            random.shuffle(valores)
            print('Valores',valores)
            prediccion = modelo.predict([valores])
            prediccion = np.array(prediccion)
            return resultado[1], prediccion

    def administrar_prestamos(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'SELECT Cantidad FROM libros WHERE idLibro = %s'
            valores = (datos['idLibro'],)
            if self.ejecutar_select_datos(sql, valores)[0] != False:
                sql = 'UPDATE libros SET Cantidad = Cantidad - 1 WHERE idLibro = %s'
                valores = (datos['idLibro'],)
                self.ejecutar_sql(sql, valores)
                print(self.sesion)
                id = self.generar_id('librosprestados')
                fecha_prestamo = datetime.datetime.now() + timedelta(days=1)
                fecha_devolucion = fecha_prestamo + timedelta(days=30)
                sql = 'INSERT INTO librosprestados (idPrestado, idUsuario, idLibro, FechaPrestamo, FechaDevolusion) VALUES (%s, %s, %s, %s, %s)'
                valores = (id, self.sesion['id'], datos['idLibro'], fecha_prestamo, fecha_devolucion)
                return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE librosprestados SET idUsuario = %s, idLibro = %s, FechaPrestamo = %s, FechaDevolusion = %s WHERE idPrestado = %s'
            valores = (datos['idUsuario'], datos['idLibro'], datos['fechaPrestamo'], datos['fechaDevolusion'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM librosprestados WHERE idPrestado = %s'
            valores = (datos['idPrestado'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT librosprestados.idPrestado, libros.idLibro, libros.Titulo, usuarios.idUsuario, usuarios.Nombre, tipocuenta.Descripcion AS Tipo_Cuenta, librosprestados.FechaPrestamo, librosprestados.FechaDevolusion FROM librosprestados INNER JOIN libros ON librosprestados.idLibro = libros.idLibro INNER JOIN usuarios ON librosprestados.idUsuario = usuarios.idUsuario INNER JOIN tipocuenta ON usuarios.idTipo = tipocuenta.idTipo'
            return self.ejecutar_mostrar_sql(sql)

        elif datos['accion'] == 'mostrar_a':
            sql = 'SELECT libros.idLibro, libros.Titulo, libros.Autor, libros.Edicion, libros.Sinopsis, libros.Imagen, libros.Cantidad, GROUP_CONCAT(generos.Nombre) AS Generos, GROUP_CONCAT(generos.idGenero) AS idGeneros, usuarios.idUsuario, usuarios.Nombre, librosprestados.FechaPrestamo, librosprestados.FechaDevolusion FROM librosprestados INNER JOIN libros ON librosprestados.idLibro = libros.idLibro INNER JOIN usuarios ON librosprestados.idUsuario = usuarios.idUsuario INNER JOIN generolibro ON libros.idLibro = generolibro.idLibro INNER JOIN generos ON generolibro.idGenero = generos.idGenero WHERE librosprestados.idUsuario = %s GROUP BY libros.idLibro ORDER BY idPrestado DESC'
            valores = (self.sesion['id'],)
            return self.ejecutar_select_datos(sql, valores)

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
            id = self.generar_id('generos')
            valores = (id, datos['nombre'], datos['descripcion'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE generos SET Nombre = %s, Descripcion = %s WHERE idGenero = %s'
            valores = (datos['nombre'], datos['descripcion'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM generolibro WHERE idGenero = %s'
            valores = (datos['id'],)
            if self.ejecutar_sql(sql, valores) == True:
                sql = 'DELETE FROM generos WHERE idGenero = %s'
                valores = (datos['id'],)
                return self.ejecutar_sql(sql, valores)
            else:
                return False

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT * FROM generos'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_estanterias(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO estanteria (idUsario, idLibro) VALUES (%s, %s)'
            valores = (self.sesion['id'], datos['idLibro'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE estanteria SET idUsario = %s, idLibro = %s WHERE idUsario = %s AND idLibro = %s'
            valores = (datos['idUsuario'], datos['idLibro'], datos['idUsuario'], datos['idLibro'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM estanteria WHERE idUsario = %s AND idLibro = %s'
            valores = (datos['idUsuario'], datos['idLibro'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT estanteria.idUsario, estanteria.idLibro, libros.idLibro, libros.Titulo, usuarios.idUsuario, usuarios.Nombre FROM estanteria INNER JOIN libros ON estanteria.idLibro = libros.idLibro INNER JOIN usuarios ON estanteria.idUsario = usuarios.idUsuario'
            return self.ejecutar_mostrar_sql(sql)

        elif datos['accion'] == 'mostrar_a':
            sql = 'SELECT libros.idLibro, libros.Titulo, libros.Autor, libros.Edicion, libros.Sinopsis, libros.Imagen, libros.Cantidad, GROUP_CONCAT(generos.Nombre) AS Generos, GROUP_CONCAT(generos.idGenero) AS idGeneros, usuarios.idUsuario, usuarios.Nombre FROM estanteria INNER JOIN libros ON estanteria.idLibro = libros.idLibro INNER JOIN usuarios ON estanteria.idUsario = usuarios.idUsuario INNER JOIN generolibro ON libros.idLibro = generolibro.idLibro INNER JOIN generos ON generolibro.idGenero = generos.idGenero WHERE estanteria.idUsario = %s GROUP BY libros.idLibro ORDER BY idLibro DESC'
            valores = (self.sesion['id'],)
            return self.ejecutar_select_datos(sql, valores)

    def administrar_prediccion(self, datos):
        sql = 'SELECT libros.Titulo, generos.Nombre, libro.Autor, libros.Sinopsis, libros.Imagen FROM libros INNER JOIN generolibro ON libros.idLibro = generolibro.idLibro INNER JOIN generos ON generolibro.idGenero = generos.idGenero INNER JOIN autores ON libros.idAutor = autores.idAutor WHERE generos.idGenero = %s'
        valores = (datos['idGenero'],)
        return self.ejecutar_select_datos(sql, valores)

    def registro(self):
        if self.sesion['inicio'] == True:
            return True
        else:
            return False

    def admin(self):
        if self.sesion['tipo'] == 1:
            return True
        else:
            return False
        
    def salir(self):
        self.sesion['inicio'] = False
        self.sesion['id'] = 'None'
        self.sesion['usuario'] = 'None'
        self.sesion['tipo'] = 'None'
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
            self.sesion['tipo'] = resultado[1][0]['idTipo']
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
        # Redirigir para el path /administrar
        elif self.path == '/administrar':
            if crud.registro() == True:
                print('Administrador:',crud.admin())
                if crud.admin() == True:
                    self.path = '/administrar.html'
                    return SimpleHTTPRequestHandler.do_GET(self)
                else:
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
            
            prediccion = {}
            for i in range(len(resultado[1][0])):
                prediccion[i] = resultado[1][0][i]
            print(prediccion)



            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(prediccion).encode('utf-8'))
            # #Convertir el ndarray a un array normal
            # prediccion = []
            # for recomendacion in resultado[1][0]:
            #     prediccion.append(recomendacion)
            # print(prediccion)
            
            # self.wfile.write(prediccion.encode('utf-8'))
        
        elif self.path == '/mostrar_generos':
            resultado = crud.administra_generos({'accion':'mostrar'})
            print(resultado[1])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_prestamos':
            resultado = crud.administrar_prestamos({'accion':'mostrar'})
            print(resultado[1])
            for prestamo in resultado[1]:
                prestamo['FechaPrestamo'] = str(prestamo['FechaPrestamo'])
                prestamo['FechaDevolusion'] = str(prestamo['FechaDevolusion'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_prestamos_a':
            resultado = crud.administrar_prestamos({'accion':'mostrar_a'})
            print(resultado[1])
            for prestamo in resultado[1]:
                prestamo['Edicion'] = str(prestamo['Edicion'])
                prestamo['FechaPrestamo'] = str(prestamo['FechaPrestamo'])
                prestamo['FechaDevolusion'] = str(prestamo['FechaDevolusion'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_estanteria_a':
            resultado = crud.administrar_estanterias({'accion':'mostrar_a'})
            print(resultado[1])
            for estanteria in resultado[1]:
                estanteria['Edicion'] = str(estanteria['Edicion'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        else:
            return SimpleHTTPRequestHandler.do_GET(self)
    
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

        elif self.path == '/administrar_libro':
            respuesta = crud.administrar_libros(data)
            if data['accion'] == 'insertar' and respuesta[0] == True:
                matriz = data["imagen"]
                matriz = [matriz[i:i+300] for i in range(0, len(matriz), 300)]

                matriz = np.array(matriz)
                print(matriz.shape)
                id_libro = respuesta[1]
                im = Image.fromarray((matriz).astype(np.uint8))
                im.save("imagenes/portadas/front"+str(id_libro)+".jpg")
                print(matriz.shape)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/administrar_usuarios':
            respuesta = crud.administrar_cuentas(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/administrar_generos':
            respuesta = crud.administra_generos(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/prestar':
            print(data)
            respuesta = crud.administrar_prestamos(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/agregar_estanteria':
            respuesta = crud.administrar_estanterias(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

print('Iniciando servidor')
httpd = HTTPServer(('localhost', 3000), servidorBasico)
httpd.serve_forever()