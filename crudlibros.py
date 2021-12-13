import conexion

conexion = conexion.conex()

class crudlibros():
    def administrar_libros(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO libros (idLibro, Titulo, Autor, Edicion, Sinopsis, Imagen, Cantidad) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            id = conexion.generar_id('libros')
            valores = (id, datos['titulo'], datos['autor'], datos['edicion'], datos['sinopsis'], 'imagenes/portadas/front'+str(id)+'.png', datos['cantidad'])
            if conexion.ejecutar_sql(sql, valores) == True:
                for genero in datos['generos']:
                    sql = 'INSERT INTO generolibro (idLibro, idGenero) VALUES (%s, %s)'
                    valores = (id, genero)
                    conexion.ejecutar_sql(sql, valores)
                return True, id
            else:
                return False

        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE libros SET Titulo = %s, Autor = %s, Edicion = %s, Sinopsis = %s, Imagen = %s, Cantidad = %s WHERE idLibro = %s'
            valores = (datos['titulo'], datos['autor'], datos['edicion'], datos['sinopsis'], 'imagenes/portadas/front'+str(datos['id'])+'.png', datos['cantidad'], datos['id'])
            if conexion.ejecutar_sql(sql, valores) == True:
                sql = 'DELETE FROM generolibro WHERE idLibro = %s'
                valores = (datos['id'],)
                if conexion.ejecutar_sql(sql, valores) == True:
                    for genero in datos['generos']:
                        sql = 'INSERT INTO generolibro (idLibro, idGenero) VALUES (%s, %s)'
                        valores = (datos['id'], genero)
                        conexion.ejecutar_sql(sql, valores)
                    return True, None
            else:
                return False

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM generolibro WHERE idLibro = %s'
            valores = (datos['id'],)
            if conexion.ejecutar_sql(sql, valores) == True:
                sql = 'DELETE FROM libros WHERE idLibro = %s'
                valores = (datos['id'],)
                if conexion.ejecutar_sql(sql, valores) == True:
                    return True
                else:
                    return False

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT libros.idLibro, libros.Titulo, libros.Autor, libros.Edicion, libros.Sinopsis, libros.Imagen, libros.Cantidad, GROUP_CONCAT(generos.Nombre) AS Generos, GROUP_CONCAT(generos.idGenero) AS idGeneros FROM libros LEFT JOIN generolibro ON libros.idLibro = generolibro.idLibro LEFT JOIN generos ON generolibro.idGenero = generos.idGenero GROUP BY libros.idLibro'
            return conexion.ejecutar_mostrar_sql(sql)