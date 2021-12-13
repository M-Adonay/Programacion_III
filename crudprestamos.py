import conexion
import datetime
from datetime import timedelta

conexion = conexion.conex()

class crudprestamos():
    def administrar_prestamos(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'SELECT Cantidad FROM libros WHERE idLibro = %s'
            valores = (datos['idLibro'],)
            if conexion.ejecutar_select_datos(sql, valores)[0] != False:
                sql = 'UPDATE libros SET Cantidad = Cantidad - 1 WHERE idLibro = %s'
                valores = (datos['idLibro'],)
                conexion.ejecutar_sql(sql, valores)
                id = conexion.generar_id('librosprestados')
                fecha_prestamo = datetime.datetime.now() + timedelta(days=1)
                fecha_devolucion = fecha_prestamo + timedelta(days=30)
                sql = 'INSERT INTO librosprestados (idPrestado, idUsuario, idLibro, FechaPrestamo, FechaDevolusion) VALUES (%s, %s, %s, %s, %s)'
                valores = (id, datos['idUsuario'], datos['idLibro'], fecha_prestamo, fecha_devolucion) #self.sesion['id']
                return conexion.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE librosprestados SET idUsuario = %s, idLibro = %s, FechaPrestamo = %s, FechaDevolusion = %s WHERE idPrestado = %s'
            valores = (datos['idUsuario'], datos['idLibro'], datos['fechaPrestamo'], datos['fechaDevolusion'], datos['id'])
            return conexion.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT librosprestados.idPrestado, libros.idLibro, libros.Titulo, usuarios.idUsuario, usuarios.Nombre, tipocuenta.Descripcion AS Tipo_Cuenta, librosprestados.FechaPrestamo, librosprestados.FechaDevolusion FROM librosprestados INNER JOIN libros ON librosprestados.idLibro = libros.idLibro INNER JOIN usuarios ON librosprestados.idUsuario = usuarios.idUsuario INNER JOIN tipocuenta ON usuarios.idTipo = tipocuenta.idTipo'
            return conexion.ejecutar_mostrar_sql(sql)

        elif datos['accion'] == 'mostrar_a':
            sql = 'SELECT libros.idLibro, libros.Titulo, libros.Autor, libros.Edicion, libros.Sinopsis, libros.Imagen, libros.Cantidad, GROUP_CONCAT(generos.Nombre) AS Generos, GROUP_CONCAT(generos.idGenero) AS idGeneros, usuarios.idUsuario, usuarios.Nombre, librosprestados.FechaPrestamo, librosprestados.FechaDevolusion FROM librosprestados INNER JOIN libros ON librosprestados.idLibro = libros.idLibro INNER JOIN usuarios ON librosprestados.idUsuario = usuarios.idUsuario INNER JOIN generolibro ON libros.idLibro = generolibro.idLibro INNER JOIN generos ON generolibro.idGenero = generos.idGenero WHERE librosprestados.idUsuario = %s GROUP BY libros.idLibro ORDER BY idPrestado DESC'
            valores = (datos['id'],) #self.sesion['id']
            return conexion.ejecutar_select_datos(sql, valores)