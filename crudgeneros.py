import conexion

conexion = conexion.conex()

class curdgeneros():
    def administra_generos(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO generos (idGenero, Nombre, Descripcion) VALUES (%s, %s, %s)'
            id = conexion.generar_id('generos')
            valores = (id, datos['nombre'], datos['descripcion'])
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE generos SET Nombre = %s, Descripcion = %s WHERE idGenero = %s'
            valores = (datos['nombre'], datos['descripcion'], datos['id'])

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM generolibro WHERE idGenero = %s'
            valores = (datos['id'],)
            if conexion.ejecutar_sql(sql, valores) == True:
                sql = 'DELETE FROM generos WHERE idGenero = %s'
                valores = (datos['id'],)
                return conexion.ejecutar_sql(sql, valores)
            else:
                return False

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT * FROM generos'
            return conexion.ejecutar_mostrar_sql(sql)

        return conexion.ejecutar_sql(sql, valores)