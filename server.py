from os import name
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import crudestanteria
import crudgeneros
import crudlibros
import crudusuarios
import crudprestamos
import crudtipocuenta
import crudrating

crudestanteria = crudestanteria.crudestanteria()
crudgeneros = crudgeneros.curdgeneros()
crudlibros = crudlibros.crudlibros()
crudusuarios = crudusuarios.crudusuarios()
crudprestamos = crudprestamos.crudprestamos()
crudtipocuenta = crudtipocuenta.crudtipocuenta()
crudrating = crudrating.crudrating()

from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

sesion = {'inicio': False, 'id':'None', 'nick':'None', 'tipo':'None','contra':'None'}

class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        global sesion
        self.sesion = sesion
        #Redirigir para el path /
        print(self.sesion)
        if self.path == '/':
            if sesion['inicio'] == True:
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /index
        elif self.path == '/index':
            if sesion['inicio'] == True:
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        # Redirigir para el path /administrar
        elif self.path == '/administrar':
            if sesion['inicio'] == True:
                print('Administrador:',sesion['tipo'])
                if sesion['tipo'] == 1:
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
            if sesion['inicio'] == True:
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /cuenta
        elif self.path == '/cuenta':
            if sesion['inicio'] == True:
                self.path = '/cuenta.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /estanteria
        elif self.path == '/estanteria':
            if sesion['inicio'] == True:
                self.path = '/estanteria.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /recomedaciones
        elif self.path == '/recomendaciones':
            if sesion['inicio'] == True:
                self.path = '/recomendaciones.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /tendencias
        elif self.path == '/tendencias':
            if sesion['inicio'] == True:
                self.path = '/tendencias.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /prestamos
        elif self.path == '/prestamos':
            if sesion['inicio'] == True:
                self.path = '/prestamos.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /libroasad
        elif self.path == '/librosad':
            if sesion['inicio'] == True:
                self.path = '/librosad.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /usuariosad
        elif self.path == '/usuariosad':
            if sesion['inicio'] == True:
                self.path = '/usuariosad.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        #Redirigir para el path /prestamosad
        elif self.path == '/prestamosad':
            if sesion['inicio'] == True:
                self.path = '/prestamosad.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/mostrar_libros':
            resultado = crudlibros.administrar_libros({'accion':'mostrar'})
            print(resultado[0])
            for libro in resultado[1]:
                libro['Edicion'] = str(libro['Edicion'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_usuarios_a':
            resultado = crudusuarios.administrar_cuentas({'accion':'mostrar_a', 'id':sesion['id']})
            print(resultado)
            for usuario in resultado[1]:
                usuario['FechaNacimiento'] = str(usuario['FechaNacimiento'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_usuarios':
            resultado = crudusuarios.administrar_cuentas({'accion':'mostrar'})
            print(resultado)
            for usuario in resultado[1]:
                usuario['FechaNacimiento'] = str(usuario['FechaNacimiento'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_recomendaciones':
            resultado = crudusuarios.administrar_cuentas({'accion':'mostrar_favoritos', 'id':sesion['id']})
            print(resultado[1][0])
            
            prediccion = {}
            for i in range(len(resultado[1][0])):
                prediccion[i] = resultado[1][0][i]
            print(prediccion)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(prediccion).encode('utf-8'))
        
        elif self.path == '/mostrar_generos':
            resultado = crudgeneros.administra_generos({'accion':'mostrar'})
            print(resultado[1])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_prestamos':
            resultado = crudprestamos.administrar_prestamos({'accion':'mostrar'})
            print(resultado[1])
            for prestamo in resultado[1]:
                prestamo['FechaPrestamo'] = str(prestamo['FechaPrestamo'])
                prestamo['FechaDevolusion'] = str(prestamo['FechaDevolusion'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_prestamos_a':
            resultado = crudprestamos.administrar_prestamos({'accion':'mostrar_a', 'id': sesion['id']})
            print('PRESTAMOS PARA' + sesion['nick'], resultado[1])
            for prestamo in resultado[1]:
                prestamo['Edicion'] = str(prestamo['Edicion'])
                prestamo['FechaPrestamo'] = str(prestamo['FechaPrestamo'])
                prestamo['FechaDevolusion'] = str(prestamo['FechaDevolusion'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_estanteria_a':
            resultado = crudestanteria.administrar_estanterias({'accion':'mostrar_a', 'id': sesion['id']})
            print(resultado[1])
            for estanteria in resultado[1]:
                estanteria['Edicion'] = str(estanteria['Edicion'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado[1])).encode('utf-8'))

        elif self.path == '/mostrar_rating':
            resultado = crudrating.administrar_ratings({'accion':'listar'})
            print(resultado)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado)).encode('utf-8'))

        elif self.path == '/recomendar':
            ratings = crudrating.administrar_ratings({'accion':'listar'})
            print(ratings)
            csv_ratings = []
            for rating in ratings[1]:
                csv_ratings.append([rating['idUsuario'], rating['idLibro'], rating['valoracion']])
            df_ratings = pd.DataFrame(csv_ratings, columns=['idUsuario', 'idLibro', 'rating'])
            print(df_ratings)
            corr_matrix = df_ratings.corr()
            print(corr_matrix)
            corr_matrix.to_csv('corr_matrix.csv')


            print(csv_ratings)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = ratings)).encode('utf-8'))
            

        else:
            return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        global sesion
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode('utf-8')
        data = json.loads(data)

        if self.path == '/iniciar_sesion':
            print(data)
            respuesta = crudusuarios.administrar_sesion(data)
            print(respuesta)
            if respuesta[0] == True:
                print('Inicio de sesion correcto')
                sesion['id'] = respuesta[1]['id']
                sesion['inicio'] = True
                sesion['nombre'] = respuesta[1]['nombre']
                sesion['nick'] = respuesta[1]['nickname']
                sesion['tipo'] = respuesta[1]['tipo']

                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(dict({'inicio':True})).encode('utf-8'))
            else:
                print('No se ha podido iniciar sesion')

        elif self.path == '/salir':
            sesion['inicio'] = False
            sesion['id'] = None
            sesion['nombre'] = None
            sesion['nick'] = None
            sesion['tipo'] = None
            if sesion['inicio'] == False:
                print('Sesion cerrada')
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(dict({'inicio':False})).encode('utf-8'))
            else:
                print('No se ha podido cerrar sesion')

        elif self.path == '/administrar_libro':
            respuesta = crudlibros.administrar_libros(data)
            print(respuesta)
            print(data['accion'], data['accion'] == 'insertar', data['id'], data['nuevaimagen'], data['nuevaimagen'] == True)
            if data['accion'] == 'insertar' or data['nuevaimagen'] == True and respuesta[0] == True:
                imagen = np.fromstring(data['imagen'], np.uint8, sep=',')
                imagen = imagen.reshape(data['alto'], data['ancho'], 3)

                if data['accion'] == 'insertar':
                    id = respuesta[1]
                else:
                    id = data['id']

                plt.imsave('imagenes/portadas/front'+str(id)+'.png', imagen)
                print('Imagen guardada en imagenes/portadas/front'+str(id)+'.png')

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/administrar_usuarios':
            print(data)
            respuesta = crudusuarios.administrar_cuentas(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/administrar_generos':
            respuesta = crudgeneros.administra_generos(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/prestar':
            print(data)
            data['idUsuario'] = sesion['id']
            respuesta = crudprestamos.administrar_prestamos(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/agregar_estanteria':
            data['id'] = sesion['id']
            respuesta = crudestanteria.administrar_estanterias(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/rating':
            data['idUsuario'] = sesion['id']
            print('TODOS LOS DATOS', data)
            respuesta = crudrating.administrar_ratings(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(respuesta = respuesta)).encode('utf-8'))

        elif self.path == '/mostrar_ratings':
            data['idUsuario'] = sesion['id']
            data['accion'] = 'mostrar'
            resultado = crudrating.administrar_ratings(data)
            print('RATINGS PARA EL USUARIO' + str(sesion['id']),resultado)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resultado = resultado)).encode('utf-8'))


print('Iniciando servidor')
httpd = HTTPServer(('localhost', 3000), servidorBasico)
httpd.serve_forever()