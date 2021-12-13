import conexion

conexion = conexion.conex()

class crudestanteria():
    def administrar_estanterias(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO estanteria (idUsario, idLibro) VALUES (%s, %s)'
            valores = (datos['id'], datos['idLibro']) # self.session['id']
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE estanteria SET idUsario = %s, idLibro = %s WHERE idUsario = %s AND idLibro = %s'
            valores = (datos['idUsuario'], datos['idLibro'], datos['idUsuario'], datos['idLibro'])

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM estanteria WHERE idUsario = %s AND idLibro = %s'
            valores = (datos['idUsuario'], datos['idLibro'])

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT estanteria.idUsario, estanteria.idLibro, libros.idLibro, libros.Titulo, usuarios.idUsuario, usuarios.Nombre FROM estanteria INNER JOIN libros ON estanteria.idLibro = libros.idLibro INNER JOIN usuarios ON estanteria.idUsario = usuarios.idUsuario'
            return conexion.ejecutar_mostrar_sql(sql)

        elif datos['accion'] == 'mostrar_a':
            sql = 'SELECT libros.idLibro, libros.Titulo, libros.Autor, libros.Edicion, libros.Sinopsis, libros.Imagen, libros.Cantidad, GROUP_CONCAT(generos.Nombre) AS Generos, GROUP_CONCAT(generos.idGenero) AS idGeneros, usuarios.idUsuario, usuarios.Nombre FROM estanteria INNER JOIN libros ON estanteria.idLibro = libros.idLibro INNER JOIN usuarios ON estanteria.idUsario = usuarios.idUsuario INNER JOIN generolibro ON libros.idLibro = generolibro.idLibro INNER JOIN generos ON generolibro.idGenero = generos.idGenero WHERE estanteria.idUsario = %s GROUP BY libros.idLibro ORDER BY idLibro DESC'
            valores = (datos['id'],) # self.session['id']
            return conexion.ejecutar_select_datos(sql, valores)

        return conexion.ejecutar_sql(sql, valores)