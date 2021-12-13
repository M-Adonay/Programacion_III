import conexion

conexion = conexion.conex()

class crudtipocuenta():
    def administrar_tipo_cuentas(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO tipocuenta (idTipo, Descripcion) VALUES (%s, %s)'
            valores = (datos['id'], datos['descripcion'])
            return conexion.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE tipocuenta SET Descripcion = %s WHERE idTipo = %s'
            valores = (datos['descripcion'], datos['id'])
            return conexion.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM tipocuenta WHERE idTipo = %s'
            valores = (datos['id'],)
            return conexion.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT * FROM tipocuenta'
            return conexion.ejecutar_mostrar_sql(sql)