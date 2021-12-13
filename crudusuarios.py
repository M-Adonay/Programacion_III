import conexion
import random
import numpy as np

conexion = conexion.conex()

class crudusuarios:
    def administrar_cuentas(self, datos):
        if datos['accion'] == 'insertar':
            print(datos)
            sql = 'INSERT INTO usuarios (idUsuario, Dui, Nombre, Nickname, Telefono, Correo, Direccion, FechaNacimiento, Contraseña, idTipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            id = conexion.generar_id('usuarios')
            valores = (id, datos['dui'], datos['nombre'], datos['nickname'], datos['telefono'], datos['correo'], datos['direccion'], datos['fechaNacimiento'], datos['contraseña'], datos['idTipo'])
     
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE usuarios SET Dui = %s, Nombre = %s, Nickname = %s, Telefono = %s, Correo = %s, Direccion = %s, FechaNacimiento = %s, Contraseña = %s, idTipo = %s WHERE idUsuario = %s'
            valores = (datos['dui'], datos['nombre'], datos['nickname'], datos['telefono'], datos['correo'], datos['direccion'], datos['fechaNacimiento'], datos['contraseña'], datos['idTipo'], datos['id'])

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM usuarios WHERE idUsuario = %s'
            valores = (datos['id'],)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT usuarios.idUsuario, usuarios.Dui, usuarios.Nombre, usuarios.Nickname, usuarios.Telefono, usuarios.Correo, usuarios.Direccion, usuarios.FechaNacimiento, usuarios.Contraseña, usuarios.idTipo, tipocuenta.Descripcion AS Tipo FROM usuarios LEFT JOIN tipocuenta ON usuarios.idTipo = tipocuenta.idTipo'
            return conexion.ejecutar_mostrar_sql(sql)
        
        elif datos['accion'] == 'mostrar_a':
            sql = 'SELECT usuarios.idUsuario, usuarios.Dui, usuarios.Nombre, usuarios.Nickname, usuarios.Telefono, usuarios.Correo, usuarios.Direccion, usuarios.FechaNacimiento, usuarios.Contraseña, tipocuenta.idTipo, tipocuenta.Descripcion FROM usuarios LEFT JOIN tipocuenta ON usuarios.idTipo = tipocuenta.idTipo WHERE usuarios.idUsuario = %s'
            valores = (datos['id'],) #self.sesion['id']
            return conexion.ejecutar_select_datos(sql, valores)

        elif datos['accion'] == 'mostrar_favoritos':
            print(datos) #self.sesion
            sql = 'SELECT usuarios.Nombre, GROUP_CONCAT(generos.idGenero) AS Generos FROM usuarios LEFT JOIN librosprestados ON usuarios.idUsuario = librosprestados.idUsuario LEFT JOIN libros ON librosprestados.idLibro = libros.idLibro LEFT JOIN generolibro ON libros.idLibro = generolibro.idLibro LEFT JOIN generos ON generolibro.idGenero = generos.idGenero WHERE usuarios.idUsuario = %s GROUP BY generos.idGenero ORDER BY librosprestados.idPrestado DESC LIMIT 10'
            valores = (datos['id'],) #self.sesion['id']
            resultado = conexion.ejecutar_select_datos(sql, valores)
            print(resultado)
            generos = []
            etiquetas = []
            if resultado != False:
                if resultado[0]['Generos'] != None:
                    for i in range(len(resultado[1])):
                        generos.append(len(resultado[1][i]['Generos'].split(',')))

                        print('Longitud en generos')
            print('Longitudes',generos)
            
            # if len(generos) < 10:
            #     for i in range(10-len(generos)):
            #         generos.append(0)
            # print('Longitudes',generos)
            # valores = []
            # # 
            # for i in range(4):
            #     valores.append(max(generos))
            #     generos.remove(max(generos))
            
            # random.shuffle(valores)
            # print('Valores',valores)
            # prediccion = modelo.prediccion([valores])
            # prediccion = np.array(prediccion)
            return resultado[1], ['prediccion']

        return conexion.ejecutar_sql(sql, valores)

    def administrar_sesion(self, datos):
        sql = 'SELECT * FROM usuarios WHERE Nickname = %s AND Contraseña = %s'
        valores = (datos['usuario'], datos['contra'])
        resultado = conexion.ejecutar_select_datos(sql, valores)
        if resultado[0] == True:
            sesion = {'inicio': True, 'id': resultado[1][0]['idUsuario'], 'nombre': resultado[1][0]['Nombre'], 'nickname': resultado[1][0]['Nickname'], 'tipo': resultado[1][0]['idTipo']}
            # self.sesion['inicio'] = True
            # self.sesion['id'] = resultado[1][0]['idUsuario']
            # self.sesion['usuario'] = resultado[1][0]['Nickname']
            # self.sesion['tipo'] = resultado[1][0]['idTipo']
            # self.sesion['contra'] = resultado[1][0]['Contraseña']
            return True, sesion
        else:
            sesion = {'inicio': False, 'id': None, 'nombre': None, 'nickname': None, 'tipo': None}
            return False, sesion