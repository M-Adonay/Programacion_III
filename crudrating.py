from re import S
import conexion

conexion = conexion.conex()

class crudrating:
    def administrar_ratings(self, data):
        try:
            print('DATOS EN RATING',data)
            if data['accion'] == 'insertar':
                sql = "INSERT INTO rating (idLibro, idUsuario, valoracion) VALUES (%s, %s, %s)"
                valores = (data['idLibro'], data['idUsuario'], data['rating'])
            
            elif data['accion'] == 'actualizar':
                sql = "UPDATE rating SET valoracion = %s WHERE idLibro = %s AND idUsuario = %s"
                valores = (data['rating'], data['idUsuario'], data['idLibro'])

            elif data['accion'] == 'eliminar':
                sql = "DELETE FROM rating WHERE idLibro = %s AND idUsuario = %s"
                valores = (data['idUsuario'], data['idLibro'])

            elif data['accion'] == 'mostrar':
                print('DATOS EN RATING',data)
                sql = f"SELECT * FROM rating WHERE idLibro = {data['idLibro']} AND idUsuario = {data['idUsuario']}"
                print(sql)
                return conexion.ejecutar_mostrar_sql(sql)

            elif data['accion'] == 'listar':
                sql = "SELECT * FROM rating"
                valores = ()
                return conexion.ejecutar_mostrar_sql(sql)

            return conexion.ejecutar_sql(sql, valores)
        except:
            return False